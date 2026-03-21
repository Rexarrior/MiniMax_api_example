#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

MODEL="${MODEL:-music-2.5+}"
INSTRUMENTAL="${INSTRUMENTAL:-0}"

BODY=$(MODEL="$MODEL" INSTRUMENTAL="$INSTRUMENTAL" python3 -c '
import json, os
model = os.environ["MODEL"]
instr = os.environ.get("INSTRUMENTAL", "0") == "1"
req = {
  "model": model,
  "prompt": "Indie folk, melancholic, short demo clip.",
  "stream": False,
  "output_format": "hex",
  "audio_setting": {"sample_rate": 44100, "bitrate": 256000, "format": "mp3"},
}
if instr and "2.5+" in model:
  req["is_instrumental"] = True
else:
  req["lyrics"] = (
    "[verse]\\nQuiet streets and amber light\\n"
    "Footsteps fade into the night\\n"
    "[chorus]\\nHold the moment, soft and slow\\n"
  )
  req["lyrics_optimizer"] = False
print(json.dumps(req))
')

RESP=$(curl_minimax_json POST "/v1/music_generation" "$BODY")
if ! python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('base_resp',{}).get('status_code')==0 else 1)" <<<"$RESP"; then
  echo "$RESP" | python3 -m json.tool >&2
  exit 1
fi

if [[ "${MINIMAX_RAW_JSON:-0}" == "1" ]]; then
  echo "$RESP"
else
  echo "$RESP" | python3 -m json.tool
fi
