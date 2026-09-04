import logging

import pytest

from conftest import BASE_URL

log = logging.getLogger("he-pytest.posts")


@pytest.mark.smoke
def test_get_all_posts(api):
    log.info("GET /posts")
    resp = api.get(f"{BASE_URL}/posts")
    assert resp.status_code == 200
    posts = resp.json()
    assert len(posts) == 100
    log.info("got %d posts", len(posts))


@pytest.mark.smoke
def test_get_single_post(api):
    log.info("GET /posts/1")
    resp = api.get(f"{BASE_URL}/posts/1")
    assert resp.status_code == 200
    post = resp.json()
    assert post["id"] == 1
    assert post["userId"] == 1
    assert post["title"]


@pytest.mark.regression
def test_create_post(api):
    log.info("POST /posts")
    payload = {"title": "he-pytest", "body": "hello", "userId": 1}
    resp = api.post(f"{BASE_URL}/posts", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    assert created["title"] == "he-pytest"
    assert "id" in created


@pytest.mark.regression
def test_posts_filtered_by_user(api):
    log.info("GET /posts?userId=2")
    resp = api.get(f"{BASE_URL}/posts", params={"userId": 2})
    assert resp.status_code == 200
    posts = resp.json()
    assert len(posts) > 0
    assert all(p["userId"] == 2 for p in posts)


@pytest.mark.regression
def test_post_not_found(api):
    """Deliberately FAILING test — jsonplaceholder returns 404 {} for id 999,
    and this assertion intentionally expects an id back to demo a failure row."""
    log.info("GET /posts/999 (deliberate failure)")
    resp = api.get(f"{BASE_URL}/posts/999")
    body = resp.json()
    assert body.get("id") == 999, "expected post 999 to exist (deliberate failure)"
