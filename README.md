# Real-Time Chat Backend

FastAPI backend for a real-time one-to-one chat application. It provides JWT authentication, PostgreSQL persistence, Alembic migrations, REST endpoints, and authenticated WebSocket messaging.

## Features

- User registration and JWT login
- Authenticated `/auth/me` endpoint
- PostgreSQL persistence with SQLAlchemy
- Alembic database migrations
- Real-time messaging over authenticated WebSockets
- Pending message delivery after reconnecting

## Requirements

- Python 3.11+
- PostgreSQL 14+

## Setup

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
pip install -r requirements.txt
```

Windows PowerShell activation:

```powershell
.\venv\Scripts\Activate.ps1
```

Create `.env` from `.env.example`, create the PostgreSQL database named in `DATABASE_URL`, and run migrations:

```bash
alembic upgrade head
```

Start the API:

```bash
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000`. Interactive documentation is available at `/docs`.

## Environment

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/realtime_chat
SECRET_KEY=replace-this-with-a-long-random-secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Never commit `.env` or real secrets. Commit only `.env.example`.

## REST API

- `POST /auth/register` creates a user with `username` and `password`.
- `POST /auth/login` returns a bearer access token.
- `GET /auth/me` returns the current user and requires `Authorization: Bearer <token>`.
- `GET /users/` lists users and requires a bearer token.

## WebSocket

Connect with the JWT returned by `/auth/login`:

```text
ws://127.0.0.1:8000/ws?token=<access-token>
```

Send messages as JSON:

```json
{
  "receiver": 2,
  "message": "Hello"
}
```

Incoming messages contain `id`, `user`, `receiver`, `message`, and `created_at`.

## Migrations

After changing SQLAlchemy models, generate and review a migration:

```bash
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

## Structure

```text
core/        Configuration and security
database/    SQLAlchemy engine and sessions
model/       SQLAlchemy models
schema/      Pydantic schemas
service/     Business logic
api/         REST endpoints
webSocket/   WebSocket routes and connection management
alembic/     Database migrations
```
