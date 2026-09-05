import logging

import pytest

from conftest import BASE_URL
from helpers import assert_schema, poll_until, retry_on_flake, wait_until

log = logging.getLogger("he-pytest.posts")

POST_SCHEMA = {"userId": int, "id": int, "title": str, "body": str}

POST_IDS = [1, 2, 42, 99]
USER_IDS = [1, 3, 5, 7, 10]


@pytest.mark.smoke
def test_get_all_posts(api):
    log.info("GET /posts")
    resp = api.get(f"{BASE_URL}/posts")
    assert resp.status_code == 200
    posts = resp.json()
    assert len(posts) == 100
    for post in posts[:10]:
        assert_schema(post, POST_SCHEMA)
    log.info("got %d posts", len(posts))


@pytest.mark.smoke
@pytest.mark.parametrize("post_id", POST_IDS)
def test_get_single_post(api, post_id):
    log.info("GET /posts/%d", post_id)
    resp = api.get(f"{BASE_URL}/posts/{post_id}")
    assert resp.status_code == 200
    post = resp.json()
    assert_schema(post, POST_SCHEMA)
    assert post["id"] == post_id
    assert post["title"]


@pytest.mark.regression
def test_create_post(api):
    log.info("POST /posts")
    payload = {"title": "he-pytest", "body": "hello", "userId": 1}
    resp = api.post(f"{BASE_URL}/posts", json=payload)
    assert resp.status_code == 201
    created = resp.json()
    assert_schema(created, POST_SCHEMA)
    assert created["title"] == "he-pytest"


@pytest.mark.regression
@pytest.mark.parametrize("user_id", USER_IDS)
def test_posts_filtered_by_user(api, user_id):
    log.info("GET /posts?userId=%d", user_id)
    resp = api.get(f"{BASE_URL}/posts", params={"userId": user_id})
    assert resp.status_code == 200
    posts = resp.json()
    assert len(posts) > 0
    for post in posts:
        assert_schema(post, POST_SCHEMA)
        assert post["userId"] == user_id


@pytest.mark.regression
@pytest.mark.parametrize("post_id", POST_IDS)
def test_post_responds_within_deadline(api, post_id):
    """wait_until: the endpoint must answer with a 200 inside 5s."""
    def fetch():
        r = api.get(f"{BASE_URL}/posts/{post_id}")
        return r if r.status_code == 200 else None

    resp = wait_until(fetch, timeout=5.0, interval=0.5, desc=f"GET /posts/{post_id} 200")
    assert_schema(resp.json(), POST_SCHEMA)


@pytest.mark.regression
def test_poll_post_comments_until_non_empty(api):
    """poll_until: poll the comments sub-resource until it returns >=5 rows."""
    comments = poll_until(
        fn=lambda: api.get(f"{BASE_URL}/posts/1/comments").json(),
        predicate=lambda rows: isinstance(rows, list) and len(rows) >= 5,
        timeout=10.0, interval=1.0, desc="post 1 comments >= 5",
    )
    assert all(c["postId"] == 1 for c in comments)


@pytest.mark.regression
@retry_on_flake(retries=2, delay=0.5)
def test_update_post_title_with_retry(api):
    """retry_on_flake: PUTs against jsonplaceholder occasionally hiccup;
    the decorator absorbs a transient failure and logs each retry."""
    log.info("PUT /posts/1")
    resp = api.put(
        f"{BASE_URL}/posts/1",
        json={"id": 1, "title": "updated-by-he-pytest", "body": "b", "userId": 1},
    )
    assert resp.status_code == 200
    updated = resp.json()
    assert_schema(updated, POST_SCHEMA)
    assert updated["title"] == "updated-by-he-pytest"


@pytest.mark.regression
def test_post_not_found(api):
    """Deliberately FAILING test — jsonplaceholder returns 404 {} for id 999,
    and this assertion intentionally expects an id back to demo a failure row."""
    log.info("GET /posts/999 (deliberate failure)")
    resp = api.get(f"{BASE_URL}/posts/999")
    body = resp.json()
    assert body.get("id") == 999, "expected post 999 to exist (deliberate failure)"
