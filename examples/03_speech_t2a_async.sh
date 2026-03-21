#!/usr/bin/env bash
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=examples/common.sh
source "$DIR/common.sh"

MODEL="${MODEL:-speech-2.8-hd}"

BODY=$(MODEL="$MODEL" python3 -c '
import json, os
print(json.dumps({
  "model": os.environ["MODEL"],
  "text": "This is a short async MiniMax speech demo.",
  "language_boost": "auto",
  "voice_setting": {
    "voice_id": "English_expressive_narrator",
    "speed": 1,
    "vol": 1,
    "pitch": 0,
  },
  "audio_setting": {
    "audio_sample_rate": 32000,
    "bitrate": 128000,
    "format": "mp3",
    "channel": 2,
  },
}))
')

CREATE_RESP=$(curl_minimax_json POST "/v1/t2a_async_v2" "$BODY")
if ! python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('base_resp',{}).get('status_code')==0 else 1)" <<<"$CREATE_RESP"; then
  echo "$CREATE_RESP" | python3 -m json.tool >&2
  exit 1
fi

TASK_ID=$(python3 -c "import json,sys; print(json.load(sys.stdin)['task_id'])" <<<"$CREATE_RESP")
echo "task_id=$TASK_ID"

for _ in $(seq 1 120); do
  Q=$(curl_minimax_json GET "/v1/query/t2a_async_query_v2?task_id=${TASK_ID}")
  ST=$(python3 -c "import json,sys; print(str(json.load(sys.stdin).get('status','')).lower())" <<<"$Q")
  if [[ "$ST" == "success" ]]; then
    FILE_ID=$(python3 -c "import json,sys; print(json.load(sys.stdin).get('file_id',''))" <<<"$Q")
    echo "status=success file_id=$FILE_ID"
    R=$(curl_minimax_json GET "/v1/files/retrieve?file_id=${FILE_ID}")
    python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('file',{}).get('download_url',''))" <<<"$R"
    exit 0
  fi
  if [[ "$ST" == "failed" || "$ST" == "expired" ]]; then
    echo "$Q" | python3 -m json.tool >&2
    exit 1
  fi
  sleep 2
done

echo "Timeout waiting for async speech" >&2
exit 1
