# Full Stack Software Developer for Spacecraft Collision Avoidance Software task

## Project requirements (tested in Linux)

* Python 3.12
* [uv](https://docs.astral.sh/uv/getting-started/installation/)
* [pnpm](https://pnpm.io/)
* [docker](https://docs.docker.com/engine/install/)
* [compose](https://docs.docker.com/compose/install/)

## Setup

1. Create .env file with a valid DISCOWEB token:

   ```sh
   DISCOWEB_TOKEN=XXX
   ```
 
1. ./scripts/docker-build.sh
1. docker-compose up
   
   Start all services, run migrations and download 2025-01-01 to 2025-01-31 data from discoweb api.

   Must be ready:
   - Postgres: http://localhost:5050
   - Backend: http://localhost:8000/docs
   - Frontend: http://localhost:3000

## Checks

The tests require the services ready and Postgres populated with data

### Backend

1. cp .env backend
2. cd backend
1. uv sync
1. uv run pytest
1. uv run ruff check

### Frontend

1. cd frontend
2. pnpm install
1. pnpm test
1. pnpm lint


## Explanation

The task was implemented with these components:
- Backend by Fastapi with the following services:: 
  - /download_data/: Call discoweb-api and populate the local postgres
  - /get_space_objects_variation/: Compute the difference between launches and reentries per day
- Frontend by Vite, React. Use the backend and plot the differences by day
