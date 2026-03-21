#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

TASK_ID="${TASK_ID:-${1:-}}"
if [[ -z "$TASK_ID" ]]; then
  echo "Usage: TASK_ID=<id> $0   or   $0 <task_id>" >&2
  exit 1
fi

OUT_DIR="$DIR/../out"
mkdir -p "$OUT_DIR"
OUT_FILE="${OUT_FILE:-$OUT_DIR/video_${TASK_ID}.mp4}"

for _ in $(seq 1 180); do
  Q=$(curl_minimax_json GET "/v1/query/video_generation?task_id=${TASK_ID}")
  if ! python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('base_resp',{}).get('status_code')==0 else 1)" <<<"$Q"; then
    echo "$Q" | python3 -m json.tool >&2
    exit 1
  fi
  ST=$(python3 -c "import json,sys; print(str(json.load(sys.stdin).get('status','')))" <<<"$Q")
  lower=$(echo "$ST" | tr '[:upper:]' '[:lower:]')
  if [[ "$lower" == "success" ]]; then
    FILE_ID=$(python3 -c "import json,sys; print(json.load(sys.stdin).get('file_id',''))" <<<"$Q")
    echo "file_id=$FILE_ID"
    R=$(curl_minimax_json GET "/v1/files/retrieve?file_id=${FILE_ID}")
    URL=$(python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('file',{}).get('download_url','') or '')" <<<"$R")
    if [[ -z "$URL" ]]; then
      echo "$R" | python3 -m json.tool >&2
      exit 1
    fi
    curl -sS -L -o "$OUT_FILE" "$URL"
    echo "Wrote $OUT_FILE"
    exit 0
  fi
  if [[ "$lower" == "fail" ]]; then
    echo "$Q" | python3 -m json.tool >&2
    exit 1
  fi
  sleep 3
done

echo "Timeout waiting for video task" >&2
exit 1
