import os
from pathlib import Path

from fastapi.testclient import TestClient


def make_client(tmp_path, monkeypatch):
    db_path = tmp_path / "test.sqlite3"
    monkeypatch.setenv("TODO_DB_PATH", str(db_path))
    import importlib
    import app.main as main
    importlib.reload(main)
    return TestClient(main.app)


def test_register_login_create_and_list_todo(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)

    res = client.post("/register", data={"email": "ada@example.com", "password": "secret123"}, follow_redirects=False)
    assert res.status_code == 303

    res = client.post("/todos", data={"title": "Ship polished todo app"}, follow_redirects=False)
    assert res.status_code == 303

    page = client.get("/")
    assert page.status_code == 200
    assert "Ship polished todo app" in page.text
    assert "ada@example.com" in page.text


def test_todos_are_isolated_between_users(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)

    client.post("/register", data={"email": "ada@example.com", "password": "secret123"})
    client.post("/todos", data={"title": "Ada private task"})
    client.get("/logout")

    client.post("/register", data={"email": "grace@example.com", "password": "secret123"})
    page = client.get("/")

    assert "grace@example.com" in page.text
    assert "Ada private task" not in page.text


def test_auth_validation_and_duplicate_registration(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)

    first = client.post("/register", data={"email": "ada@example.com", "password": "secret123"})
    assert first.status_code == 200
    client.get("/logout")

    duplicate = client.post("/register", data={"email": "ada@example.com", "password": "another123"})
    assert "Account already exists" in duplicate.text

    bad_login = client.post("/login", data={"email": "ada@example.com", "password": "wrong"})
    assert "Invalid email or password" in bad_login.text


def test_toggle_and_delete_are_scoped_to_owner(tmp_path, monkeypatch):
    client = make_client(tmp_path, monkeypatch)

    client.post("/register", data={"email": "ada@example.com", "password": "secret123"})
    client.post("/todos", data={"title": "Ada task"})
    client.get("/logout")

    client.post("/register", data={"email": "grace@example.com", "password": "secret123"})
    # Grace cannot mutate Ada's first todo.
    toggle = client.post("/todos/1/toggle", follow_redirects=False)
    delete = client.post("/todos/1/delete", follow_redirects=False)
    assert toggle.status_code == 404
    assert delete.status_code == 404
