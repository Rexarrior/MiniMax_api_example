#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

MODE="${MODE:-write_full_song}"
PROMPT="${PROMPT:-A cheerful love song about a summer day at the beach}"

BODY=$(MODE="$MODE" PROMPT="$PROMPT" python3 -c '
import json, os
print(json.dumps({
  "mode": os.environ["MODE"],
  "prompt": os.environ["PROMPT"],
}))
')

RESP=$(curl_minimax_json POST "/v1/lyrics_generation" "$BODY")
if ! python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('base_resp',{}).get('status_code')==0 else 1)" <<<"$RESP"; then
  echo "$RESP" | emit_safe_json_stderr
  exit 1
fi

OUT_ROOT="$(cd "$DIR/.." && pwd)"
echo "$RESP" | OUT_ROOT="$OUT_ROOT" MINIMAX_RAW_JSON="${MINIMAX_RAW_JSON:-0}" PYTHONPATH="$OUT_ROOT/examples_python" python3 -c '
import json, os, pathlib, re, sys
import minimax_http as mh
d = json.load(sys.stdin)
root = pathlib.Path(os.environ["OUT_ROOT"]) / "out"
root.mkdir(parents=True, exist_ok=True)
title = d.get("song_title") or "untitled"
lyrics = d.get("lyrics") or ""
slug = re.sub(r"[^0-9a-zA-Z._-]+", "_", str(title))[:100] or "lyrics"
p = root / f"lyrics_{slug}.txt"
p.write_text(title + "\n\n" + lyrics, encoding="utf-8")
print("Wrote", p, file=sys.stderr)
view = mh.json_for_console(d)
raw = os.environ.get("MINIMAX_RAW_JSON", "0") == "1"
if raw:
    print(json.dumps(view, ensure_ascii=False))
else:
    print(json.dumps(view, indent=2, ensure_ascii=False))
'
