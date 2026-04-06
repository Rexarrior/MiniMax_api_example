# Novel V2

A visual novel/text adventure game MVP.

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Frontend**: Vue 3, TypeScript, Pinia, TailwindCSS
- **Media**: Howler.js for audio, HTML5 video

## Quick Start

### Development

```bash
# Start infrastructure
docker-compose up -d postgres

# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up -d
```

## Project Structure

See `AGENTS.md` for detailed architecture documentation.
