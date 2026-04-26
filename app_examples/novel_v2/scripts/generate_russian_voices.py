#!/usr/bin/env python3
"""Generate Russian voice files for Jedi Day story."""

from __future__ import annotations

import hashlib
import sys
import time
from pathlib import Path

# Add examples_python to path for minimax_http
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "examples_python"))
import minimax_http as mh

# Paths
NOVEL_V2_ROOT = Path(__file__).parent.parent.parent.parent / "app_examples" / "novel_v2"
VOICES_DIR = NOVEL_V2_ROOT / "stories" / "jedi_day" / "assets" / "voices"

# Character voice settings for Russian (from MiniMax Russian voices)
RUSSIAN_VOICE_IDS = {
    "kai_tara": ("Russian_BrightHeroine", 1.0, 2),
    "master_ysanna": ("Russian_AmbitiousWoman", 0.85, -3),
    "chewbacca": ("Russian_ReliableMan", 0.9, 5),
    "darth_varek": ("Russian_Bad-temperedBoy", 1.1, -8),
    "tarri": ("Russian_PessimisticGirl", 1.2, 6),
    "Boushh": ("Russian_AttractiveGuy", 0.8, -2),
}

# All 51 Russian dialogues to generate
RUSSIAN_DIALOGUES = [
    {"speaker": "kai_tara", "text": "Чуивака! Сейчас!", "hash": "cd9503cb52"},
    {"speaker": "kai_tara", "text": "Храм тёмной стороны больше не существует. Вуки в безопасности.", "hash": "4ae274820c"},
    {"speaker": "kai_tara", "text": "Храм Дагорр? Я чувствовала это место. Это культовое место ситхов.", "hash": "991ac411fe"},
    {"speaker": "kai_tara", "text": "Адепт ситхов. Опасен, но не Мастер. Мы справимся.", "hash": "1e138cb6a3"},
    {"speaker": "kai_tara", "text": "Оставайся здесь, малыш. Я его верну.", "hash": "61a9e2003d"},
    {"speaker": "kai_tara", "text": "У меня нет времени на переговоры. Сколько?", "hash": "db5b4abc14"},
    {"speaker": "kai_tara", "text": "Договорились. В путь.", "hash": "0f8c78b6a7"},
    {"speaker": "kai_tara", "text": "Мастер! Я почувствовала возмущение. Что-то тёмное пробудилось.", "hash": "ca5a7a410d"},
    {"speaker": "kai_tara", "text": "Ситхи? Здесь? Я думала, они были уничтожены.", "hash": "10ab9257ce"},
    {"speaker": "kai_tara", "text": "Лес... он прекрасен. Вуки живут здесь поколениями.", "hash": "127727f3c2"},
    {"speaker": "kai_tara", "text": "Вот! Эти показания совпадают с возмущением, которое я почувствовала.", "hash": "5f5ea72cba"},
    {"speaker": "kai_tara", "text": "Отпусти пленников, ситх. Этот храм принадлежит прошлому.", "hash": "949c4a8751"},
    {"speaker": "kai_tara", "text": "Свобода через страх и боль? Тёмная сторона развращает.", "hash": "d634ac68a4"},
    {"speaker": "kai_tara", "text": "Ты видел что-то... или кого-то. Кто обратил тебя ко тьме?", "hash": "662b797f51"},
    {"speaker": "kai_tara", "text": "Что-то не так. Холодная тьма... Я никогда ничего подобного не чувствовала.", "hash": "16786317ad"},
    {"speaker": "kai_tara", "text": "Это чувство... это не просто возмущение. Это присутствие.", "hash": "1bbf789c0d"},
    {"speaker": "kai_tara", "text": "Нет эмоций — есть покой.", "hash": "b2d9aa6fc8"},
    {"speaker": "kai_tara", "text": "Это был лишь один храм. Варек говорил о мастере... грядёт большая тьма.", "hash": "4a58dbdef4"},
    {"speaker": "kai_tara", "text": "Я Кай-Тара Вен. И да, малыш, я чувствую в тебе Силу.", "hash": "afdbc62c0e"},
    {"speaker": "kai_tara", "text": "Нет эмоций... есть только покой!", "hash": "f0f0d182e8"},
    {"speaker": "kai_tara", "text": "Я сделала то, что было необходимо. Но Мастер... как думаете, придёт ли мастер Варека?", "hash": "f11241d356"},
    {"speaker": "kai_tara", "text": "Тогда я буду готова. Сила направит меня.", "hash": "d338d6c8f4"},
    {"speaker": "kai_tara", "text": "Сила течёт через всё живое. Лес говорит со мной.", "hash": "4baebfe758"},
    {"speaker": "kai_tara", "text": "Эти сигналы... они исходят из Тёмных Земель.", "hash": "0b9b901c83"},
    {"speaker": "kai_tara", "text": "Чуивака! Нет!", "hash": "36eacea02a"},
    {"speaker": "kai_tara", "text": "R-22, следуй на координаты Кашиикка. Максимальная скорость.", "hash": "e18cd29d93"},
    {"speaker": "kai_tara", "text": "Тёмная сторона сильна здесь. Я чувствую, как она давит на мой разум.", "hash": "34e8d38ea8"},
    {"speaker": "chewbacca", "text": "Рвааааа! (Спасибо, друг!)", "hash": "bb7fe5033f"},
    {"speaker": "chewbacca", "text": "Тричоппа был похищен тёмным. Мой племянник... он исследовал старые тропы.", "hash": "3390f313a2"},
    {"speaker": "chewbacca", "text": "Ррааа! (Тёмный — он носит красные мечи, говорит о древней силе)", "hash": "a36370f5e8"},
    {"speaker": "chewbacca", "text": "Ррааа рвааа рвааа! (Она спасла всех нас! Джедай — настоящий герой!)", "hash": "d4d5562c3f"},
    {"speaker": "chewbacca", "text": "Кай-Тара! Хвала звёздам, ты здесь. Нам нужна твоя помощь.", "hash": "50c62ad793"},
    {"speaker": "chewbacca", "text": "Кай-Тара! Тричоппа! Нужна помощь! Тёмные атакуют!", "hash": "8f2cd8d87a"},
    {"speaker": "tarri", "text": "Пожалуйста, спаси моего дядю! Я что угодно сделаю!", "hash": "04797ac08f"},
    {"speaker": "tarri", "text": "Ты сделала это! Ты правда сделала это!", "hash": "b00285dfbb"},
    {"speaker": "tarri", "text": "Ты правда Джедай? Ты можешь научить меня использовать Силу?", "hash": "49a910758e"},
    {"speaker": "Boushh", "text": "Врооаааа! (Это задание опасно. Тёмный убил троих моих людей.)", "hash": "64644ffd4d"},
    {"speaker": "Boushh", "text": "Врарврар! (Пять тысяч кредитов. Плюс расходы.)", "hash": "89a9b102a1"},
    {"speaker": "master_ysanna", "text": "Я знаю, моя юная ученица. Я отслеживаю это присутствие уже несколько дней.", "hash": "b1ec1f8519"},
    {"speaker": "master_ysanna", "text": "Остатки ситхов. Древнее святилище было реактивировано на тёмной стороне Кашиикка.", "hash": "8aa838a8ee"},
    {"speaker": "master_ysanna", "text": "Зло никогда по-настоящему не умирает, Кай-Тара. Возьми мой истребитель. Чуивака ждёт тебя в деревне.", "hash": "6667f0f330"},
    {"speaker": "master_ysanna", "text": "Ты справилась с ситуацией хорошо, моя ученица. Ты становишься сильнее.", "hash": "41c57a1b78"},
    {"speaker": "master_ysanna", "text": "Тёмная сторона всегда будет подниматься снова. И Джедаи всегда будут рядом, чтобы противостоять ей.", "hash": "b62a31e015"},
    {"speaker": "darth_varek", "text": "Джедай... как мило. Ещё один ягнёнок на заклание.", "hash": "0c81067d1b"},
    {"speaker": "darth_varek", "text": "Прошлое? Это святилище хранит секреты самого Марка Рэгноса!", "hash": "ca7ae79c9d"},
    {"speaker": "darth_varek", "text": "Преклонись к тёмной стороне, или смотри, как твой союзник умрёт.", "hash": "3fc50a93ca"},
    {"speaker": "darth_varek", "text": "Вы, джедаи, говорите о балансе, но храните власть. Я предлагаю свободу!", "hash": "78b8666ffb"},
    {"speaker": "darth_varek", "text": "Разврат? Теперь я вижу ясно. Сенат гнил. Джедаи — глупцы.", "hash": "b815dc901f"},
    {"speaker": "darth_varek", "text": "Молчи! Ты ничего не знаешь!", "hash": "3f7e77e96c"},
    {"speaker": "darth_varek", "text": "Твоя техника безупречна... но ярость сильнее!", "hash": "c9461a84c9"},
    {"speaker": "darth_varek", "text": "Если я не могу получить эту силу... ты тоже не получишь!", "hash": "fd229014b1"},
]


def generate_voice(speaker: str, text: str, voice_hash: str) -> Path | None:
    """Generate a single Russian voice file."""
    if speaker not in RUSSIAN_VOICE_IDS:
        print(f"  No voice config for {speaker}, skipping")
        return None

    voice_id, speed, pitch = RUSSIAN_VOICE_IDS[speaker]

    # Create filename: ru_voice_{speaker}_{hash}_{speed}_{pitch}.mp3
    filename = f"ru_voice_{speaker}_{voice_hash}_{speed}_{pitch}.mp3"
    dest = VOICES_DIR / filename

    # Skip if already exists
    if dest.exists():
        print(f"  Already exists: {filename}")
        return dest

    print(f"  Generating: {filename}")
    print(f"    Text: {text[:50]}...")

    try:
        result = mh.generate_speech(text, voice_id, dest, speed, pitch)
        if result:
            print(f"  SUCCESS: {filename}")
            return dest
        else:
            print(f"  FAILED: {filename}")
            return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def main() -> None:
    print("Russian Voice Generation for Jedi Day")
    print(f"Output directory: {VOICES_DIR}")
    print(f"Total dialogues to generate: {len(RUSSIAN_DIALOGUES)}")
    print()

    VOICES_DIR.mkdir(parents=True, exist_ok=True)

    results = {}
    for i, d in enumerate(RUSSIAN_DIALOGUES, 1):
        print(f"[{i}/{len(RUSSIAN_DIALOGUES)}] {d['speaker']}:")
        result = generate_voice(d['speaker'], d['text'], d['hash'])
        results[f"{d['speaker']}_{d['hash']}"] = result

        # Rate limiting - wait between requests
        if result:
            print(f"  Waiting 2 seconds...")
            time.sleep(2)

    # Summary
    print(f"\n{'='*60}")
    print("GENERATION COMPLETE")
    print(f"{'='*60}")
    success = sum(1 for r in results.values() if r is not None)
    print(f"Successfully generated: {success}/{len(RUSSIAN_DIALOGUES)}")

    failed = [k for k, v in results.items() if v is None]
    if failed:
        print(f"Failed: {len(failed)}")
        for f in failed:
            print(f"  - {f}")


if __name__ == "__main__":
    main()