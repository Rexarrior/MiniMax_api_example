#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

PROMPT="${PROMPT:-A man in a white t-shirt, full-body, standing outdoors, photorealistic, soft daylight.}"

BODY=$(PROMPT="$PROMPT" python3 -c '
import json, os
print(json.dumps({
  "model": "image-01",
  "prompt": os.environ["PROMPT"],
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 1,
  "prompt_optimizer": False,
}))
')

RESP=$(curl_minimax_json POST "/v1/image_generation" "$BODY")
if ! python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('base_resp',{}).get('status_code')==0 else 1)" <<<"$RESP"; then
  echo "$RESP" | emit_safe_json_stderr
  exit 1
fi

OUT_ROOT="$(cd "$DIR/.." && pwd)"
echo "$RESP" | OUT_ROOT="$OUT_ROOT" MINIMAX_RAW_JSON="${MINIMAX_RAW_JSON:-0}" PYTHONPATH="$OUT_ROOT/examples_python" python3 -c '
import json, os, pathlib, sys, urllib.request
import minimax_http as mh
d = json.load(sys.stdin)
root = pathlib.Path(os.environ["OUT_ROOT"]) / "out"
root.mkdir(parents=True, exist_ok=True)
urls = (d.get("data") or {}).get("image_urls") or []
for i, u in enumerate(urls):
    dest = root / f"image_t2i_{i}.jpeg"
    req = urllib.request.Request(str(u), headers={"User-Agent": "minimax_explore/1"})
    with urllib.request.urlopen(req, timeout=120) as r:
        dest.write_bytes(r.read())
    print("Wrote", dest, file=sys.stderr)
view = mh.json_for_console(d)
raw = os.environ.get("MINIMAX_RAW_JSON", "0") == "1"
if raw:
    print(json.dumps(view, ensure_ascii=False))
else:
    print(json.dumps(view, indent=2, ensure_ascii=False))
'
