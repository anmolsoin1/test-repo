import logging

import pytest

from conftest import BASE_URL
from helpers import assert_schema, retry_on_flake, wait_until

log = logging.getLogger("he-pytest.users")

USER_SCHEMA = {
    "id": int,
    "name": str,
    "username": str,
    "email": str,
    "phone": str,
    "website": str,
    "address": {
        "street": str,
        "suite": str,
        "city": str,
        "zipcode": str,
        "geo": {"lat": str, "lng": str},
    },
    "company": {"name": str, "catchPhrase": str, "bs": str},
}

USER_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.mark.smoke
def test_get_all_users(api):
    log.info("GET /users")
    resp = api.get(f"{BASE_URL}/users")
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) == 10
    for user in users:
        assert_schema(user, USER_SCHEMA)


@pytest.mark.smoke
@pytest.mark.parametrize("user_id", USER_IDS)
def test_get_user_by_id(api, user_id):
    log.info("GET /users/%d", user_id)
    resp = api.get(f"{BASE_URL}/users/{user_id}")
    assert resp.status_code == 200
    user = resp.json()
    assert_schema(user, USER_SCHEMA)
    assert user["id"] == user_id


@pytest.mark.regression
@pytest.mark.parametrize("user_id", USER_IDS[:5])
def test_user_todos(api, user_id):
    log.info("GET /users/%d/todos", user_id)
    resp = api.get(f"{BASE_URL}/users/{user_id}/todos")
    assert resp.status_code == 200
    todos = resp.json()
    assert len(todos) > 0
    for todo in todos:
        assert_schema(todo, {"userId": int, "id": int, "title": str, "completed": bool})
        assert todo["userId"] == user_id


@pytest.mark.regression
@retry_on_flake(retries=1, delay=0.5)
def test_user_albums_endpoint_available(api):
    """wait_until + retry_on_flake combined: wait for a 200, retry once."""
    def fetch():
        r = api.get(f"{BASE_URL}/users/1/albums")
        return r if r.status_code == 200 else None

    resp = wait_until(fetch, timeout=5.0, interval=0.5, desc="GET /users/1/albums 200")
    albums = resp.json()
    assert len(albums) > 0
    for album in albums:
        assert_schema(album, {"userId": int, "id": int, "title": str})
        assert album["userId"] == 1
