#!/usr/bin/env bash
# Было в корневом examples/07: INSTRUMENTAL=1 + model music-2.5+ → is_instrumental (вне таблицы Token Plan).
# Из корня репозитория:
#   bash archive/token_plan_deprecated/examples/07_music_generation_music-2.5plus_instrumental.sh
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$DIR/../../.." && pwd)"
# shellcheck source=examples/common.sh
source "$ROOT/examples/common.sh"

MODEL="${MODEL:-music-2.5+}"
INSTRUMENTAL="${INSTRUMENTAL:-1}"

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
  echo "$RESP" | emit_safe_json_stderr
  exit 1
fi

echo "$RESP" | OUT_ROOT="$ROOT" MODEL="$MODEL" MINIMAX_RAW_JSON="${MINIMAX_RAW_JSON:-0}" PYTHONPATH="$ROOT/examples_python" python3 -c '
import binascii, json, os, pathlib, re, sys
import minimax_http as mh
d = json.load(sys.stdin)
root = pathlib.Path(os.environ["OUT_ROOT"]) / "out"
root.mkdir(parents=True, exist_ok=True)
model = os.environ["MODEL"]
safe = re.sub(r"[^0-9a-zA-Z._-]+", "_", model)
hex_audio = d.get("data", {}).get("audio")
if isinstance(hex_audio, str) and hex_audio.strip():
    p = root / f"music_{safe}.mp3"
    p.write_bytes(binascii.unhexlify(hex_audio.encode("ascii")))
    print("Wrote", p, file=sys.stderr)
view = mh.json_for_console(d)
raw = os.environ.get("MINIMAX_RAW_JSON", "0") == "1"
if raw:
    print(json.dumps(view, ensure_ascii=False))
else:
    print(json.dumps(view, indent=2, ensure_ascii=False))
'
