#!/usr/bin/env bash
# Запуск по одному разу всех примеров под модели Token Plan (без audio-to-text / STT).
# Из корня репозитория:  bash scripts/run_token_plan_models.sh
#
# Переменные окружения:
#   SKIP_VIDEO=1       — не создавать и не опрашивать видео (долго).
#   SKIP_ASYNC_SPEECH=1 — пропустить асинхронный TTS (6× ожидание).
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
 echo "WARNING: Running the full test suite can use roughly 25,000–30,000 API requests from your quota. Consider running the tests in smaller batches. Set WARNING_READED=1 in the environment to acknowledge this and proceed."
 exit 1
fi

mkdir -p out

run() { echo ""; echo "=== $* ==="; }

run "01 text (MiniMax-M2.7)"
python3 examples/01_text_anthropic.py
echo

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

  run "04 T2V MiniMax-Hailuo-02 (768P 6s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-02 DURATION=6 RESOLUTION=768P bash examples/04_video_t2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_02_768p6s_${TID}.mp4" bash examples/06_video_poll.sh

  run "05 I2V MiniMax-Hailuo-2.3-Fast (768P 6s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-2.3-Fast DURATION=6 RESOLUTION=768P bash examples/05_video_i2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_23fast_${TID}.mp4" bash examples/06_video_poll.sh

  MiniMax-Hailuo-02 @ 512P: только I2V (нужен first_frame_image); чистый T2V с 512P API отклоняет.
  run "05 I2V MiniMax-Hailuo-02 (512P 6s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-02 DURATION=6 RESOLUTION=512P bash examples/05_video_i2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_02_512p6s_${TID}.mp4" bash examples/06_video_poll.sh

  run "05 I2V MiniMax-Hailuo-02 (512P 10s) → poll"
  TID=$(MODEL=MiniMax-Hailuo-02 DURATION=10 RESOLUTION=512P bash examples/05_video_i2v.sh)
  echo "task_id=$TID"
  TASK_ID="$TID" OUT_FILE="$ROOT/out/video_hailuo_02_512p10s_${TID}.mp4" bash examples/06_video_poll.sh
else
  echo ""
  echo "=== video: пропущено (SKIP_VIDEO=1) ==="
fi

export MINIMAX_RAW_JSON=1

for m in music-2.5+ music-2.5 music-2.0; do
  run "07 music: $m"
  MODEL="$m" bash examples/07_music_generation.sh | ROOT_DIR="$ROOT" MODEL_TAG="$m" python3 -c '
import binascii, json, os, pathlib, re, sys
d = json.load(sys.stdin)
root = pathlib.Path(os.environ["ROOT_DIR"]) / "out"
root.mkdir(parents=True, exist_ok=True)
print("ok status", d.get("base_resp", {}).get("status_code"), "trace", d.get("trace_id", ""))
aud = d.get("data", {}).get("audio")
if isinstance(aud, str) and aud.strip():
  safe = re.sub(r"[^0-9a-zA-Z._-]+", "_", os.environ["MODEL_TAG"])
  path = root / f"music_{safe}.mp3"
  path.write_bytes(binascii.unhexlify(aud))
  print("wrote", path)
else:
  print("(no hex audio in response; mp3 not saved)")
'
done

run "08 lyrics"
bash examples/08_lyrics_generation.sh | ROOT_DIR="$ROOT" python3 -c '
import json, os, pathlib, re, sys
d = json.load(sys.stdin)
root = pathlib.Path(os.environ["ROOT_DIR"]) / "out"
root.mkdir(parents=True, exist_ok=True)
title = d.get("song_title") or "untitled"
body = d.get("lyrics") or ""
print("title:", title)
print("lyrics_len:", len(body))
slug = re.sub(r"[^0-9a-zA-Z._-]+", "_", title)[:100] or "lyrics"
path = root / f"lyrics_{slug}.txt"
path.write_text(title + "\n\n" + body, encoding="utf-8")
print("wrote", path)
'

run "09 image T2I image-01"
bash examples/09_image_t2i.sh | ROOT_DIR="$ROOT" python3 -c '
import json, os, pathlib, sys, urllib.request
d = json.load(sys.stdin)
root = pathlib.Path(os.environ["ROOT_DIR"]) / "out"
urls = d.get("data", {}).get("image_urls") or []
print("urls:", urls)
for i, u in enumerate(urls):
  req = urllib.request.Request(u, headers={"User-Agent": "minimax_explore/1"})
  dest = root / f"image_t2i_{i}.jpeg"
  with urllib.request.urlopen(req, timeout=120) as r:
    dest.write_bytes(r.read())
  print("wrote", dest)
'

run "10 image I2I image-01-live"
bash examples/10_image_i2i.sh | ROOT_DIR="$ROOT" python3 -c '
import json, os, pathlib, sys, urllib.request
d = json.load(sys.stdin)
root = pathlib.Path(os.environ["ROOT_DIR"]) / "out"
urls = d.get("data", {}).get("image_urls") or []
print("urls:", urls)
for i, u in enumerate(urls):
  req = urllib.request.Request(u, headers={"User-Agent": "minimax_explore/1"})
  dest = root / f"image_i2i_{i}.jpeg"
  with urllib.request.urlopen(req, timeout=120) as r:
    dest.write_bytes(r.read())
  print("wrote", dest)
'

echo ""
echo "Готово. Артефакты в out/ (аудио/видео при успехе)."
