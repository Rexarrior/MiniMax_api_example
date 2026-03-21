#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

PROMPT="${PROMPT:-A girl looking into the distance from a library window, cinematic light.}"
SUBJECT_IMAGE="${SUBJECT_IMAGE:-https://cdn.hailuoai.com/prod/2025-08-12-17/video_cover/1754990600020238321-411603868533342214-cover.jpg}"

BODY=$(PROMPT="$PROMPT" SUBJECT_IMAGE="$SUBJECT_IMAGE" python3 -c '
import json, os
print(json.dumps({
  "model": "image-01-live",
  "prompt": os.environ["PROMPT"],
  "aspect_ratio": "16:9",
  "response_format": "url",
  "n": 1,
  "subject_reference": [
    {"type": "character", "image_file": os.environ["SUBJECT_IMAGE"]},
  ],
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
