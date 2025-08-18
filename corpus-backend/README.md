# Corpus Backend

FastAPI backend with Stickies and Tags CRUD, pagination, and tests.

## Prerequisites
- Python 3.8+
- Optional: Docker + Docker Compose

## Setup (local, virtualenv)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the API
- Using uvicorn (local):
```bash
uvicorn main:app --reload
# Server: http://127.0.0.1:8000
```
- Using Docker Compose:
```bash
docker compose up --build
# Server: http://127.0.0.1:8000
```

## Endpoints
- Health: `GET /` → `{ "message": "Welcome to Corpus API" }`
- Tags:
  - `POST /tags/` → create tag: `{ "name": "work", "parent_id": null }`
  - `GET /tags/` → list tags (supports `limit`, `offset`)
  - `GET /tags/{id}` → get by id
  - `PATCH /tags/{id}` → partial update: `{ "name": "personal", "parent_id": null }`
  - `DELETE /tags/{id}` → delete
- Stickies:
  - `POST /stickies/` → create sticky: `{ "title": "note", "content": "...", "url": null, "tag_ids": [1,2] }`
  - `GET /stickies/` → list (supports `limit`, `offset`)
  - `GET /stickies/{id}` → get by id
  - `PATCH /stickies/{id}` → partial update: any subset of `title`, `content`, `url`, `tag_ids`
  - `DELETE /stickies/{id}` → delete
  - `POST /stickies/{id}/like` → increment like_count

## Curl examples
Base URL: `http://127.0.0.1:8000`

- Create tag
```bash
curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -d '{"name":"work"}' \
  http://127.0.0.1:8000/tags/
```

- List tags (paginated)
```bash
curl -sS 'http://127.0.0.1:8000/tags?limit=10&offset=0'
```

- Create sticky with tags
```bash
curl -sS -X POST \
  -H 'Content-Type: application/json' \
  -d '{"title":"note","content":"content","url":null,"tag_ids":[1,2]}' \
  http://127.0.0.1:8000/stickies/
```

- Like a sticky
```bash
curl -sS -X POST http://127.0.0.1:8000/stickies/1/like
```

- Update a sticky (partial)
```bash
curl -sS -X PATCH \
  -H 'Content-Type: application/json' \
  -d '{"title":"updated","tag_ids":[1]}' \
  http://127.0.0.1:8000/stickies/1
```

- Delete a tag
```bash
curl -sS -X DELETE -i http://127.0.0.1:8000/tags/1
```

## Tests
Run all tests:
```bash
python -m pytest -q
```
If using plain `pytest`, ensure the venv is active or run:
```bash
.venv/bin/pytest -q
```
