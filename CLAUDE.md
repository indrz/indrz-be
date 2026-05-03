# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 1. Purpose

Indrz is an indoor mapping, fm management platform.

## 2. Read This First

Before making changes, read in this order:

1. **For Product Understanding**: Start with product specs (`docs/specification/*.md`)
2. **For Implementation**: Reference technical specs (`spec-*-techstack.md`)
3. **For Feature Dependencies**: Check "Related Specifications" sections in each doc
4. **For Writing New Specs**: Use [TEMPLATE.md](./TEMPLATE.md)

## 3. Repo Map

- `backend/` — API, Django + DRF + PostGIS, PgRouting, Geoserver
- `frontend/` — Nuxt 4 + Vue 3 + Vuetify 3 + OpenLayers
- `devops/` — dockerfiles to build images
- `docs/specification` — application specifications for AI context
- `docs/user/` — user facing documentation in both english and german


## 4. Development Commands

### Docker-first local development (recommended)

```bash
# Start all services (PostGIS, Django API, GeoServer, Nuxt dev server, Nginx)
make up

# Start only PostGIS database and Django API
make up-api

# stop only PostGIS database and Django API
make down-api

# Stop all services
make down

# Load demo/fixture data
make load-data-dev

# Run Django migrations
make migrate

# Create Django superuser
make superuser
```

### Frontend Code (from `frontend/src/`)

```bash
npm run dev          # Start dev server
npm run build        # Production build
npm run lint         # ESLint with auto-fix
npm run pw:test      # Run Playwright E2E tests
```

### Backend Code (from `backend/indrz/`)

```bash
# Run pytest inside container
docker exec -t indrz_api pytest

# Run specific test file
docker exec -t indrz_api pytest path/to/test_file.py

# Run specific test
docker exec -t indrz_api pytest path/to/test_file.py::test_function_name
```

Pytest config is in `backend/indrz/pytest.ini` (uses `--nomigrations --create-db`).

## 5. Core Engineering Rules

1. Keep changes company-scoped.
Every domain entity should be scoped to a company and company boundaries must be enforced in routes/services.

2. Keep specifications synchronized.

3. Do not replace strategic docs wholesale unless asked.
Prefer additive updates.
4. Keep plan docs dated and centralized.
New plan documents belong in `docs/plans/` and should use `YYYY-MM-DD-slug.md` filenames.

## Architecture

### URL Routing

- Nginx reverse proxy routes:
  - `/` → Nuxt frontend (port 3000)
  - `/api` → Django API (port 8000)
  - `/geoserver` → GeoServer (port 8080)
  - `/static`, `/media` → served from `backend/data/`
- API base: `/api/v1/` with Swagger docs at `/api/v1/docs/`
- Django admin: `/api/v1/admin/`

### Backend API (Django)

- Settings: `backend/indrz/settings/settings.py`
- URL config: `backend/indrz/indrz/urls.py`
- DRF router: `backend/indrz/indrz/routers.py`
- Core apps: `buildings`, `campus`, `poi_manager`, `routing`, `organizations`, `users`, `bookway`, `zoneplan`, `dxf_loader`

### Frontend Client (Nuxt 4)

- Config: `frontend/src/nuxt.config.js`
- State management: Pinia stores in `frontend/src/stores/`
- Map utilities: `frontend/src/util/` (mapHandler.js, mapLayers.js, mapStyles.js, RouteHandler.js, POIHandler.js)
- API client: `frontend/src/util/api.js` using `ofetch`
- Runtime config via env vars: `API_BASE`, `BASE_WMS_URL`, `GEOSERVER_URL`, etc.
- E2E tests: `frontend/src/playwright/` using `data-test` selectors

### Key Frontend Components

- `IndrzMap.vue` — Main map component with OpenLayers
- `LeftPanel.vue` — Navigation/search sidebar
- `FloorChanger.vue` — Floor level selector
- `drawers/` — PoiDrawer, RouteDrawer, DrawerSearch
- `admin/` — POI manager, shelf manager, zoneplan editor

## Environment Setup

1. Copy `backend/.env-example` to root `.env`
2. Run `make up` — entrypoint auto-runs migrations and collectstatic
3. Access: `http://localhost` (via Nginx) or `http://localhost:3000` (Nuxt direct)

## Code style

- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')
  
## Workflow

- Prefer running single tests, and not the whole test suite, for performance

## Golden Rules

1. **Never commit secrets** — no tokens, passwords, or `.env` contents in git
2. When modifying API endpoints, update `backend/indrz/indrz/urls.py` and/or `routers.py`, then verify Swagger renders
3. When changing proxy paths, update `devops/docker/local/nginx/conf/default-dev.conf` and ensure frontend env vars match
4. **Preserve behavior unless explicitly changing it.** Refactors must be behavior-preserving and include tests if risk exists.
5. **Keep changes scoped.** Prefer small, reviewable PRs over broad rewrites.
6. **Write tests for logic changes.** Backend logic changes require Pytest coverage; frontend behavior changes require unit/integration where applicable and/or Playwright E2E updates.
7. **Document as you go.** Any user-facing or operational change should be reflected under `/docs`.
8. **Consistency over cleverness.** Follow existing patterns in the repo.
9. **Maintain the specifications** Update all specifications with the new features keeping specifications technology agnostic and always up to date.
