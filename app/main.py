import hashlib
import hmac
import os
import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = Path(os.getenv("TODO_DB_PATH", BASE_DIR / "todo.sqlite3"))
SECRET_KEY = os.getenv("TODO_SECRET_KEY", "dev-secret-change-me")

app = FastAPI(title="Primer Executive Tasks")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, same_site="lax")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with db() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )


@app.on_event("startup")
def _startup():
    init_db()


# TestClient does not always enter lifespan unless used as a context manager;
# initialize eagerly too so imports and simple scripts are reliable.
init_db()


def hash_password(password: str, salt: Optional[bytes] = None) -> str:
    salt = salt or os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120_000)
    return f"pbkdf2_sha256${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, salt_hex, digest = stored.split("$", 2)
    except ValueError:
        return False
    if algo != "pbkdf2_sha256":
        return False
    candidate = hash_password(password, bytes.fromhex(salt_hex)).split("$", 2)[2]
    return hmac.compare_digest(candidate, digest)


def current_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    with db() as conn:
        return conn.execute("SELECT id, email FROM users WHERE id = ?", (user_id,)).fetchone()


def require_user(request: Request):
    user = current_user(request)
    if user is None:
        raise HTTPException(status_code=401, detail="Login required")
    return user


@app.get("/", response_class=HTMLResponse)
def home(request: Request, user=Depends(current_user)):
    todos = []
    if user:
        with db() as conn:
            todos = conn.execute(
                "SELECT id, title, completed, created_at FROM todos WHERE user_id = ? ORDER BY completed, id DESC",
                (user["id"],),
            ).fetchall()
    return templates.TemplateResponse(
        request,
        "index.html",
        {"request": request, "user": user, "todos": todos, "error": None},
    )


@app.post("/register", response_class=HTMLResponse)
def register(request: Request, email: str = Form(...), password: str = Form(...)):
    email = email.strip().lower()
    if len(password) < 8:
        return templates.TemplateResponse(request, "index.html", {"request": request, "user": None, "todos": [], "error": "Password must be at least 8 characters"})
    try:
        with db() as conn:
            cur = conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)", (email, hash_password(password)))
            request.session["user_id"] = cur.lastrowid
    except sqlite3.IntegrityError:
        return templates.TemplateResponse(request, "index.html", {"request": request, "user": None, "todos": [], "error": "Account already exists"})
    return RedirectResponse("/", status_code=303)


@app.post("/login", response_class=HTMLResponse)
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    email = email.strip().lower()
    with db() as conn:
        user = conn.execute("SELECT id, email, password_hash FROM users WHERE email = ?", (email,)).fetchone()
    if not user or not verify_password(password, user["password_hash"]):
        return templates.TemplateResponse(request, "index.html", {"request": request, "user": None, "todos": [], "error": "Invalid email or password"})
    request.session["user_id"] = user["id"]
    return RedirectResponse("/", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.post("/todos")
def create_todo(title: str = Form(...), user=Depends(require_user)):
    title = " ".join(title.split())
    if not title:
        return RedirectResponse("/", status_code=303)
    with db() as conn:
        conn.execute("INSERT INTO todos (user_id, title) VALUES (?, ?)", (user["id"], title[:180]))
    return RedirectResponse("/", status_code=303)


@app.post("/todos/{todo_id}/toggle")
def toggle_todo(todo_id: int, user=Depends(require_user)):
    with db() as conn:
        row = conn.execute("SELECT completed FROM todos WHERE id = ? AND user_id = ?", (todo_id, user["id"])).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Todo not found")
        conn.execute("UPDATE todos SET completed = ? WHERE id = ? AND user_id = ?", (0 if row["completed"] else 1, todo_id, user["id"]))
    return RedirectResponse("/", status_code=303)


@app.post("/todos/{todo_id}/delete")
def delete_todo(todo_id: int, user=Depends(require_user)):
    with db() as conn:
        cur = conn.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", (todo_id, user["id"]))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found")
    return RedirectResponse("/", status_code=303)
