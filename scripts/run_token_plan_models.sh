#!/usr/bin/env bash
# Запуск по одному разу всех примеров под модели Token Plan (без audio-to-text / STT).
# Из корня репозитория:  bash scripts/run_token_plan_models.sh
#
# Переменные окружения:
#   SKIP_VIDEO=1       — не создавать и не опрашивать видео (долго).
#   SKIP_ASYNC_SPEECH=1 — пропустить асинхронный TTS (2× модели Speech 2.8).
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
  echo "Нужен MINIMAX_API_KEY в .env или окружении" >&2
  exit 1
fi
WARNING_READED=${WARNING_READED:-0}
SKIP_VIDEO="${SKIP_VIDEO:-0}"
SKIP_ASYNC_SPEECH="${SKIP_ASYNC_SPEECH:-0}"


if [[ "$WARNING_READED" != "1" ]]; then
 echo "WARNING: Running the full test suite uses many API requests against your Token Plan quota. Consider running the tests in smaller batches. Set WARNING_READED=1 in the environment to acknowledge this and proceed."
 exit 1
fi

mkdir -p out

run() { echo ""; echo "=== $* ==="; }

run "01 text (MiniMax-M2.7)"
python3 examples_python/01_text_anthropic.py
echo

# Token Plan: Speech 2.8 (hd; turbo — только на некоторых планах, см. https://platform.minimax.io/docs/token-plan/intro)
SPEECH_SYNC_MODELS=(
  speech-2.8-hd
)

for m in "${SPEECH_SYNC_MODELS[@]}"; do
  safe="${m//./_}"
  run "02 sync TTS: $m"
  MODEL="$m" OUT_FILE="$ROOT/out/t2a_sync_${safe}.mp3" bash examples/02_speech_t2a_sync.sh
done

if [[ "$SKIP_ASYNC_SPEECH" != "1" ]]; then
  for m in "${SPEECH_SYNC_MODELS[@]}"; do
    run "03 async TTS: $m"
    MODEL="$m" bash examples/03_speech_t2a_async.sh
  done
else
  echo ""
  echo "=== 03 async TTS: пропущено (SKIP_ASYNC_SPEECH=1) ==="
fi

if [[ "$SKIP_VIDEO" != "1" ]]; then
  echo "video section"
  run "04 T2V MiniMax-Hailuo-2.3 → poll"
  TID=$(MODEL=MiniMax-Hailuo-2.3 bash examples/04_video_t2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_23_${TID}.mp4" bash examples/06_video_poll.sh

  run "05 I2V MiniMax-Hailuo-2.3-Fast (768P 6s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-2.3-Fast DURATION=6 RESOLUTION=768P bash examples/05_video_i2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_23fast_${TID}.mp4" bash examples/06_video_poll.sh
else
  echo ""
  echo "=== video: пропущено (SKIP_VIDEO=1) ==="
fi

export MINIMAX_RAW_JSON=1

# Token Plan: Music-2.5 (см. таблицу на https://platform.minimax.io/docs/token-plan/intro)
for m in music-2.5; do
  run "07 music: $m"
  MODEL="$m" bash examples/07_music_generation.sh | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("ok status", d.get("base_resp", {}).get("status_code"), "trace", d.get("trace_id", ""))
'
done

run "08 lyrics"
bash examples/08_lyrics_generation.sh | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("title:", d.get("song_title", ""))
print("lyrics_len:", len(d.get("lyrics", "")))
'

run "09 image T2I image-01"
bash examples/09_image_t2i.sh | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("urls:", d.get("data", {}).get("image_urls", []))
'

echo ""
echo "Готово. Артефакты в out/ (аудио/видео при успехе)."
