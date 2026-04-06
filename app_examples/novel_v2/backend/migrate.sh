#!/bin/bash
# Migration script for the novel_v2 backend
# Usage: ./migrate.sh [command]
# Commands:
#   up       - Apply all pending migrations (default)
#   down     - Roll back the last migration
#   current  - Show current migration
#   history  - Show migration history
#   revision - Create a new revision (run: ./migrate.sh revision "message")
#   check    - Check if database is up to date

set -e

# Change to backend directory (script is in backend/ directory)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Default command
CMD="${1:-up}"

case "$CMD" in
    up)
        docker-compose exec -T backend python -m alembic upgrade head
        ;;
    down)
        docker-compose exec -T backend python -m alembic downgrade -1
        ;;
    current)
        docker-compose exec -T backend python -m alembic current
        ;;
    history)
        docker-compose exec -T backend python -m alembic history
        ;;
    revision)
        MSG="${2:-new migration}"
        docker-compose exec -T backend python -m alembic revision --autogenerate -m "$MSG"
        ;;
    check)
        docker-compose exec -T backend python -m alembic validate
        ;;
    help)
        echo "Usage: ./migrate.sh [command]"
        echo ""
        echo "Commands:"
        echo "  up       - Apply all pending migrations (default)"
        echo "  down     - Roll back the last migration"
        echo "  current  - Show current migration"
        echo "  history  - Show migration history"
        echo "  revision - Create a new revision (run: ./migrate.sh revision \"message\")"
        echo "  check    - Check if database is up to date"
        ;;
    *)
        echo "Unknown command: $CMD"
        echo "Run './migrate.sh help' for usage information"
        exit 1
        ;;
esac
