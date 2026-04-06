# Database Migrations

This project uses Alembic for database migrations.

## Quick Start

Run migrations using Docker:

```bash
# Apply all pending migrations
./backend/migrate.sh up

# Roll back the last migration
./backend/migrate.sh down

# Check current migration
./backend/migrate.sh current

# Show migration history
./backend/migrate.sh history

# Create a new migration (after changing models)
./backend/migrate.sh revision "description of changes"

# Check if database is up to date
./backend/migrate.sh check
```

## Manual Commands

If you need to run alembic directly:

```bash
# Inside the backend container
docker-compose exec backend python -m alembic <command>

# With custom alembic.ini path
docker-compose exec -T backend python -m alembic -c /app/alembic.ini <command>
```

## Workflow

1. **Make model changes** - Edit files in `backend/app/models/`
2. **Create migration** - Run `./backend/migrate.sh revision "description"`
3. **Review migration** - Check the generated file in `backend/alembic/versions/`
4. **Apply migration** - Run `./backend/migrate.sh up`
5. **Test** - Verify the application works correctly

## Migration Files

Migration files are stored in `backend/alembic/versions/`. Each file follows the pattern `{revision_id}_{slug}.py`.

## Database Connection

The migration uses `psycopg2` for synchronous database connections. The connection URL is configured in `backend/alembic.ini`:

```ini
sqlalchemy.url = postgresql+psycopg2://novel:novelpassword@postgres:5432/novel
```

When running migrations locally (not in Docker), update this to:

```ini
sqlalchemy.url = postgresql+psycopg2://novel:novelpassword@localhost:5434/novel
```

## Initial Setup

When setting up a fresh database:

1. The database will be created with no tables
2. Run `./backend/migrate.sh up` to create all tables
3. The initial migration (`644c0aee8114_initial_schema.py`) is empty because the schema was already applied manually during development

## Troubleshooting

### "Read-only file system" error

The `backend/alembic` directory is mounted as read-only in Docker. The `migrate.sh` script handles this correctly. If you need to create revisions locally, you'll need to:

1. Mount the alembic directory as writable in docker-compose.yml
2. Or create migrations on your host machine and copy them to the container

### Connection refused

Make sure the postgres container is running:

```bash
docker-compose ps
```

### Migration conflict

If multiple migrations try to alter the same table, you may need to merge them or resolve conflicts manually.

## Notes

- Migrations run inside the Docker container where the database is accessible at `postgres:5432`
- The `DATABASE_URL` environment variable uses asyncpg which doesn't work with alembic's synchronous model
- Always test migrations on a development database before running on production
