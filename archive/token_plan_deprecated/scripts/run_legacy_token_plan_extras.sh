#!/usr/bin/env bash
# Модели вне текущей таблицы Token Plan (см. archive/token_plan_deprecated/README.md).
# Нужен pay-as-you-go или иной доступ к этим идентификаторам.
# Из корня репозитория: WARNING_READED=1 bash archive/token_plan_deprecated/scripts/run_legacy_token_plan_extras.sh
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"
LEGACY="$ROOT/archive/token_plan_deprecated"

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
  echo "Set WARNING_READED=1 to run this legacy suite (extra API usage)." >&2
  exit 1
fi

mkdir -p out

run() { echo ""; echo "=== $* ==="; }

SPEECH_SYNC_MODELS=(
  speech-2.8-hd
  speech-2.6-hd
  speech-02-hd
  speech-2.8-turbo
  speech-2.6-turbo
  speech-02-turbo
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
fi

if [[ "$SKIP_VIDEO" != "1" ]]; then
  run "04 T2V MiniMax-Hailuo-02 (768P 6s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-02 DURATION=6 RESOLUTION=768P bash examples/04_video_t2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_02_768p6s_${TID}.mp4" bash examples/06_video_poll.sh

  # MiniMax-Hailuo-02 @ 512P: только I2V (first_frame_image); T2V с 512P API отклоняет.
  run "05 I2V MiniMax-Hailuo-02 (512P 6s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-02 DURATION=6 RESOLUTION=512P bash examples/05_video_i2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_02_512p6s_${TID}.mp4" bash examples/06_video_poll.sh

  run "05 I2V MiniMax-Hailuo-02 (512P 10s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-02 DURATION=10 RESOLUTION=512P bash examples/05_video_i2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_02_512p10s_${TID}.mp4" bash examples/06_video_poll.sh
fi

export MINIMAX_RAW_JSON=1

for m in music-2.5+ music-2.0; do
  run "07 music: $m"
  MODEL="$m" bash examples/07_music_generation.sh | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("ok status", d.get("base_resp", {}).get("status_code"), "trace", d.get("trace_id", ""))
'
done

run "10 image I2I image-01-live"
bash "$LEGACY/examples/10_image_i2i.sh" | python3 -c '
import json, sys
d = json.load(sys.stdin)
print("urls:", d.get("data", {}).get("image_urls", []))
'

echo ""
echo "Legacy extras done. See archive/token_plan_deprecated/README.md"
