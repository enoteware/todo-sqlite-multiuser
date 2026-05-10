# Primer Executive Tasks

A practical multi-user todo app using FastAPI + SQLite, with a high-end UI driven by `DESIGN.md`.

## Design source

The design system is based on GitHub Primer foundations (`https://primer.style/foundations/`) and encoded using Google's DESIGN.md spec (`https://github.com/google-labs-code/design.md`).

## Features

- Register/login/logout
- Passwords hashed with PBKDF2-SHA256
- SQLite persistence
- Todo create/toggle/delete
- Multi-user isolation: each account only sees/mutates its own todos
- Responsive high-end interface

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>.

## Test

```bash
pytest -q
```

## GitHub hosting note

GitHub hosts the code and CI. GitHub Pages cannot run a SQLite-backed Python server directly, so this app is packaged as a GitHub-hosted repo with local/server runtime instructions. Deploying the same repo to Fly.io, Render, Railway, or a VPS will run the SQLite backend unchanged.
