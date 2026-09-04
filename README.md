# SlimDash

A reusable small-dashboard starter built as a Python/FastAPI modular monolith with a
React + Carbon frontend. The production artifact is one non-root container; SQLite data
lives at `/data/slimdash.db`, intended to be mounted as a persistent volume.

## Quick start

Prerequisites: `uv`, Python 3.12+, Node 22+, and npm.

```bash
cp .env.example .env
uv sync
make test
make frontend-install
make quality
```

For local development, run `make dev` and `make frontend-dev` in separate terminals. Vite
proxies `/api` and `/auth` to FastAPI. The API docs are at `http://localhost:8000/docs`.

For the encapsulated runtime:

```bash
docker compose up --build
```

Open `http://localhost:8000`. The named `slimdash-data` volume survives container replacement.

## OpenID Connect

Register the exact callback URI `<APP_PUBLIC_URL>/auth/callback` with the W3ID provider, then
set `W3ID_CLIENT_ID`, `W3ID_CLIENT_SECRET`, and `W3ID_DISCOVERY_URL`. Authentication is disabled
when all three are blank, which keeps local demos and tests credential-free. In production,
use HTTPS, set `APP_SECURE_COOKIES=true`, provide a random session secret of at least 32
characters through the runtime secret mechanism, and restrict `APP_ALLOWED_HOSTS`.

The browser receives only a signed, HTTP-only session cookie. Tokens remain server-side for
the request that establishes the minimal user session and are not persisted or returned to
the frontend. For larger deployments, replace cookie sessions with a server-side session
adapter.

## Structure

```text
src/slimdash/
  dashboard/   # widget domain, use cases, ports, SQLite adapter
  identity/    # user domain, authentication use case, OIDC adapter
  web/         # FastAPI inbound adapter
  bootstrap/   # configuration and composition root
frontend/      # React, TypeScript, Vite, Carbon
tests/         # isolated unit and integration tests
```

New features should be vertical modules with their own hexagon. The web layer calls use cases,
never database or identity infrastructure directly.

## Operations

Run `make help` for install, tests, linting, formatting, type checking, dependency updates,
frontend builds, and container targets. `/api/health/live` is process liveness;
`/api/health/ready` verifies SQLite readiness.

