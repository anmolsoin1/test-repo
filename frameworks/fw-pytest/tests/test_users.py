import logging

import pytest

from conftest import BASE_URL

log = logging.getLogger("he-pytest.users")


@pytest.mark.smoke
def test_get_all_users(api):
    log.info("GET /users")
    resp = api.get(f"{BASE_URL}/users")
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) == 10


@pytest.mark.smoke
def test_user_structure(api):
    log.info("GET /users/1")
    resp = api.get(f"{BASE_URL}/users/1")
    assert resp.status_code == 200
    user = resp.json()
    for field in ("id", "name", "username", "email", "address", "company"):
        assert field in user
    assert user["address"]["geo"]["lat"]


@pytest.mark.regression
def test_user_todos(api):
    log.info("GET /users/1/todos")
    resp = api.get(f"{BASE_URL}/users/1/todos")
    assert resp.status_code == 200
    todos = resp.json()
    assert len(todos) > 0
    assert all("completed" in t for t in todos)
