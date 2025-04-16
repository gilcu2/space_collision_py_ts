# Full Stack Software Developer for Spacecraft Collision Avoidance Software task

## Project requirements

* Python 3.12
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* [docker](https://docs.docker.com/engine/install/)
* [compose](https://docs.docker.com/compose/install/)

## Setup

1. uv sync
1. ./scripts/docker-build.sh
1. docker-compose up
   
   Start all services, run migrations, download 2025-03-01 to 2025-04-30 data.
   Wait  until flow-deploy logs "Your flow 'update-flow' is being served"

   Must be ready:
   - Postgres: http://localhost:5050
   - Backend: http://localhost:8000/docs
   - Frontend: http://localhost:3000/docs

## Checks

The tests require the services ready and Postgres populated with data

### Backend

1. cd backend
1. uv run pytest
1. uv run ruff check

### Frontend

1. cd frontend
1. pnpm test
1. pnpm lint


## Explanation