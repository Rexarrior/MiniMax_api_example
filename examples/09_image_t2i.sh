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
  echo "$RESP" | python3 -m json.tool >&2
  exit 1
fi

if [[ "${MINIMAX_RAW_JSON:-0}" == "1" ]]; then
  echo "$RESP"
else
  echo "$RESP" | python3 -m json.tool
fi
