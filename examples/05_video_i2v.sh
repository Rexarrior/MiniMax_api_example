#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

MODEL="${MODEL:-MiniMax-Hailuo-2.3-Fast}"
DURATION="${DURATION:-6}"
RESOLUTION="${RESOLUTION:-768P}"
FIRST_FRAME_IMAGE="${FIRST_FRAME_IMAGE:-https://cdn.hailuoai.com/prod/2024-09-18-16/user/multi_chat_file/9c0b5c14-ee88-4a5b-b503-4f626f018639.jpeg}"
VIDEO_PROMPT="${VIDEO_PROMPT:-Subtle camera push in, natural motion.}"

BODY=$(MODEL="$MODEL" DURATION="$DURATION" RESOLUTION="$RESOLUTION" FIRST_FRAME_IMAGE="$FIRST_FRAME_IMAGE" VIDEO_PROMPT="$VIDEO_PROMPT" python3 -c '
import json, os
print(json.dumps({
  "model": os.environ["MODEL"],
  "first_frame_image": os.environ["FIRST_FRAME_IMAGE"],
  "prompt": os.environ["VIDEO_PROMPT"],
  "duration": int(os.environ["DURATION"]),
  "resolution": os.environ["RESOLUTION"],
  "prompt_optimizer": True,
}))
')

RESP=$(curl_minimax_json POST "/v1/video_generation" "$BODY")
if ! python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('base_resp',{}).get('status_code')==0 else 1)" <<<"$RESP"; then
  echo "$RESP" | emit_safe_json_stderr
  exit 1
fi

TID=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d['task_id'])" <<<"$RESP")
OUT_ROOT="$(cd "$DIR/.." && pwd)"
mkdir -p "$OUT_ROOT/out"
echo "$TID" > "$OUT_ROOT/out/last_video_task_id.txt"
echo "Wrote $OUT_ROOT/out/last_video_task_id.txt" >&2
echo "$TID"
