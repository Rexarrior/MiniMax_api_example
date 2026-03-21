#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

MODEL="${MODEL:-speech-2.8-hd}"
OUT_DIR="$DIR/../out"
mkdir -p "$OUT_DIR"
OUT_FILE="${OUT_FILE:-$OUT_DIR/t2a_sync.mp3}"

BODY=$(MODEL="$MODEL" python3 -c '
import json, os
print(json.dumps({
  "model": os.environ["MODEL"],
  "text": "Hello from MiniMax synchronous text to speech.",
  "stream": False,
  "language_boost": "auto",
  "output_format": "hex",
  "voice_setting": {
    "voice_id": "English_expressive_narrator",
    "speed": 1,
    "vol": 1,
    "pitch": 0,
  },
  "audio_setting": {
    "sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 1,
  },
}))
')

RESP=$(curl_minimax_json POST "/v1/t2a_v2" "$BODY")
CODE=$(echo "$RESP" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('base_resp',{}).get('status_code',''))")
if [[ "$CODE" != "0" ]]; then
  echo "$RESP" | emit_safe_json_stderr
  exit 1
fi

echo "$RESP" | python3 -c "
import json, sys, binascii
d = json.load(sys.stdin)
hex_audio = d['data']['audio']
open(sys.argv[1], 'wb').write(binascii.unhexlify(hex_audio))
print('Wrote', sys.argv[1], file=sys.stderr)
" "$OUT_FILE"
