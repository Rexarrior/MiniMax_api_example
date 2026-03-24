# Mini-Agent: бот веб-поиска

Пример на базе [Mini-Agent](https://github.com/MiniMax-AI/Mini-Agent) и MCP-сервера [minimax_search](https://github.com/MiniMax-AI/minimax_search). Обзор фреймворка: [Mini-Agent в документации MiniMax](https://platform.minimax.io/docs/solutions/mini-agent).

## Подготовка

1. Установите [uv](https://docs.astral.sh/uv/) и убедитесь, что `uvx` доступен в `PATH` (MCP запускается через `uvx`).
2. Из корня репозитория:

   ```bash
   pip install -r app_examples/requirements-mini-agent.txt
   ```

3. В корневом `.env` задайте:
   - `MINIMAX_API_KEY` — [кабинет MiniMax](https://platform.minimax.io/)
   - `SERPER_API_KEY` — [Serper](https://serper.dev/) (нужен для инструмента **search**)
   - опционально `JINA_API_KEY` — [Jina Reader](https://jina.ai/) (для **browse**)

   Дополнительно, как в `examples_python`: `MINIMAX_TEXT_MODEL`, `MINIMAX_API_BASE`.

4. Конфиг: лежит в `config/`. Скрипт читает `config.yaml`, иначе `config-example.yaml`. Ключ API можно не дублировать в YAML, если задан `MINIMAX_API_KEY` в `.env`.

5. MCP: в репозитории есть `config/mcp-example.json`. Если создадите `config/mcp.json`, будет использоваться он; иначе загрузчик подставит `mcp-example.json` при отсутствии `mcp.json`. Скрипт сам подмешивает `MINIMAX_API_KEY` / `SERPER_API_KEY` / `JINA_API_KEY` во временный конфиг MCP: у протокола stdio у дочернего процесса по умолчанию не полное окружение, только `PATH`, `HOME` и т.п.

## Запуск

Из корня репозитория:

```bash
python app_examples/mini_agent_websearch/run_websearch_bot.py "Ваш вопрос для поиска в интернете"
```

В терминале будут цветные логи агента; итоговый ответ дублируется в конце.

## Telegram-бот (тот же агент)

Модуль [`telegram_agent_bot.py`](telegram_agent_bot.py) только пересылает текст пользователя в [`websearch_agent.run_query`](websearch_agent.py) — отдельной логики поиска нет.

1. Создайте бота у [@BotFather](https://t.me/BotFather), получите токен.
2. В корневой `.env`: `TELEGRAM_BOT_TOKEN=...` (и как раньше ключи MiniMax / Serper / опционально Jina).
3. По желанию: `TELEGRAM_ALLOWED_USER_IDS=123,456` (только целые числа; битые значения пропускаются с предупреждением в лог) и/или `TELEGRAM_ALLOWED_USER_LOGINS=user1,user2` (username без `@`, регистр не важен). Достаточно совпадения по id **или** по username. Если обе переменные заданы, но после разбора списков пусто — ограничение не применяется (в лог будет предупреждение).

Запуск из корня репозитория:

```bash
python app_examples/mini_agent_websearch/telegram_agent_bot.py
```

Одновременно обрабатывается один запрос (глобальная блокировка); длинный ответ режется на части по лимиту Telegram (4096 символов).
