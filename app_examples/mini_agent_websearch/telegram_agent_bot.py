#!/usr/bin/env python3
"""Telegram UI for the same Mini-Agent websearch pipeline as run_websearch_bot.py.

Only forwards user text to run_query; no separate search logic here.
Env: TELEGRAM_BOT_TOKEN; optional TELEGRAM_ALLOWED_USER_IDS=123,456 and/or
TELEGRAM_ALLOWED_USER_LOGINS=user1,@user2 (Telegram username, без @ в значении можно).
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import os
import sys
from dataclasses import dataclass
from pathlib import Path

# Ensure sibling imports when run as script from repo root
_PKG = Path(__file__).resolve().parent
if str(_PKG) not in sys.path:
    sys.path.insert(0, str(_PKG))

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from websearch_agent import default_config_dir, ensure_websearch_env, run_query

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("telegram_agent_bot")

TELEGRAM_MAX_MESSAGE = 4096
_AGENT_LOCK = asyncio.Lock()


@dataclass(frozen=True, slots=True)
class _TelegramAllowlist:
    ids: frozenset[int]
    usernames: frozenset[str]


def _parse_telegram_allowlist() -> _TelegramAllowlist | None:
    """Return None if access is not restricted. Invalid ID tokens are skipped with a warning."""
    raw_ids = os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "").strip()
    raw_logins = os.environ.get("TELEGRAM_ALLOWED_USER_LOGINS", "").strip()
    if not raw_ids and not raw_logins:
        return None

    ids_out: set[int] = set()
    for part in raw_ids.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            ids_out.add(int(part))
        except ValueError:
            logger.warning(
                "Skip invalid TELEGRAM_ALLOWED_USER_IDS entry (expected integer): %r",
                part,
            )

    users_out: set[str] = set()
    for part in raw_logins.split(","):
        part = part.strip().lstrip("@").lower()
        if part:
            users_out.add(part)

    if not ids_out and not users_out:
        logger.warning(
            "Allowlist env vars set but no valid user ids or logins; treating as no restriction."
        )
        return None

    return _TelegramAllowlist(ids=frozenset(ids_out), usernames=frozenset(users_out))


def _is_user_allowed(user_id: int, username: str | None, allowlist: _TelegramAllowlist) -> bool:
    if user_id in allowlist.ids:
        return True
    if allowlist.usernames and username and username.lower() in allowlist.usernames:
        return True
    return False


def _split_telegram_chunks(text: str, limit: int = TELEGRAM_MAX_MESSAGE) -> list[str]:
    if len(text) <= limit:
        return [text]
    return [text[i : i + limit] for i in range(0, len(text), limit)]


async def _keep_typing(bot, chat_id: int, stop: asyncio.Event) -> None:
    while not stop.is_set():
        try:
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        except Exception:
            pass
        try:
            await asyncio.wait_for(stop.wait(), timeout=4.0)
            break
        except TimeoutError:
            continue


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user = update.effective_user
    if not msg or not user:
        return
    allowlist = _parse_telegram_allowlist()
    if allowlist is not None and not _is_user_allowed(user.id, user.username, allowlist):
        await msg.reply_text("Доступ запрещён.")
        return
    await msg.reply_text(
        "Пришлите вопрос — запущу Mini-Agent с веб-поиском (тот же пайплайн, что и в CLI). "
        "Один запрос обрабатывается за раз."
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await cmd_start(update, context)


async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    user = update.effective_user
    if not msg or not user:
        return

    allowlist = _parse_telegram_allowlist()
    if allowlist is not None and not _is_user_allowed(
        user.id, user.username, allowlist
    ):
        await msg.reply_text("Доступ запрещён.")
        return

    text = (msg.text or "").strip()
    if not text:
        return

    if _AGENT_LOCK.locked():
        await msg.reply_text("Сейчас выполняется другой запрос. Повторите позже.")
        return

    stop_typing = asyncio.Event()
    typing_task = asyncio.create_task(
        _keep_typing(context.bot, msg.chat_id, stop_typing)
    )
    try:
        async with _AGENT_LOCK:
            try:
                answer = await run_query(text, default_config_dir())
            except Exception as e:
                logger.exception("Agent run failed")
                await msg.reply_text(f"Ошибка агента: {e}")
                return
    finally:
        stop_typing.set()
        typing_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await typing_task

    text_out = answer.strip()
    if not text_out:
        await msg.reply_text("Агент вернул пустой ответ.")
        return

    for i, chunk in enumerate(_split_telegram_chunks(text_out)):
        if i == 0:
            await msg.reply_text(chunk)
        else:
            await context.bot.send_message(chat_id=msg.chat_id, text=chunk)


def main() -> None:
    ensure_websearch_env()
    if not os.environ.get("SERPER_API_KEY", "").strip():
        print("Set SERPER_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print("Set TELEGRAM_BOT_TOKEN in .env", file=sys.stderr)
        sys.exit(1)

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    logger.info("Starting Telegram bot (polling)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
