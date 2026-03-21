#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "$ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$ROOT/.env"
  set +a
fi

if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
  echo "Set MINIMAX_API_KEY in .env or environment (see .env.example)" >&2
  exit 1
fi

export MINIMAX_API_BASE="${MINIMAX_API_BASE:-https://api.minimax.io}"

EMIT_SAFE_JSON="${ROOT}/examples_python/emit_safe_json.py"
emit_safe_json_stderr() {
  MINIMAX_RAW_JSON=0 python3 "$EMIT_SAFE_JSON" >&2
}

curl_minimax_json() {
  local method="$1"
  local path="$2"
  local body="${3:-}"
  if [[ -n "$body" ]]; then
    curl -sS -X "$method" "${MINIMAX_API_BASE}${path}" \
      -H "Authorization: Bearer ${MINIMAX_API_KEY}" \
      -H "Content-Type: application/json" \
      -d "$body"
  else
    curl -sS -X "$method" "${MINIMAX_API_BASE}${path}" \
      -H "Authorization: Bearer ${MINIMAX_API_KEY}"
  fi
}
