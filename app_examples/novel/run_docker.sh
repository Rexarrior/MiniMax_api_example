#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$REPO_ROOT/.env"

if [ ! -f "$ENV_FILE" ]; then
    echo "Error: .env not found at $ENV_FILE"
    exit 1
fi

IMAGE_NAME="novel-app"
CONTAINER_NAME="novel-app"

cp -r "$REPO_ROOT/examples_python" "$SCRIPT_DIR/"

docker build -t "$IMAGE_NAME" "$SCRIPT_DIR"

docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker run -d \
    --name "$CONTAINER_NAME" \
    --env-file "$ENV_FILE" \
    -p 8080:8080 \
    -v "${REPO_ROOT}/app_examples/novel/stories:/app/stories" \
    --restart unless-stopped \
    "$IMAGE_NAME"

echo "Novel app started on http://localhost:8080"
