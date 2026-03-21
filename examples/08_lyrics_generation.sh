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
  echo "$RESP" | python3 -m json.tool >&2
  exit 1
fi

if [[ "${MINIMAX_RAW_JSON:-0}" == "1" ]]; then
  echo "$RESP"
else
  echo "$RESP" | python3 -m json.tool
fi
