import logging

import pytest

from conftest import BASE_URL
from helpers import assert_schema, poll_until

log = logging.getLogger("he-pytest.comments")

COMMENT_SCHEMA = {"postId": int, "id": int, "name": str, "email": str, "body": str}

COMMENT_IDS = [1, 5, 50, 250, 499]
COMMENT_POST_IDS = [1, 2, 3]


@pytest.mark.smoke
def test_get_all_comments(api):
    log.info("GET /comments")
    resp = api.get(f"{BASE_URL}/comments")
    assert resp.status_code == 200
    comments = resp.json()
    assert len(comments) == 500
    for comment in comments[:10]:
        assert_schema(comment, COMMENT_SCHEMA)


@pytest.mark.smoke
@pytest.mark.parametrize("comment_id", COMMENT_IDS)
def test_get_comment_by_id(api, comment_id):
    log.info("GET /comments/%d", comment_id)
    resp = api.get(f"{BASE_URL}/comments/{comment_id}")
    assert resp.status_code == 200
    comment = resp.json()
    assert_schema(comment, COMMENT_SCHEMA)
    assert comment["id"] == comment_id
    assert "@" in comment["email"]


@pytest.mark.regression
@pytest.mark.parametrize("post_id", COMMENT_POST_IDS)
def test_comments_for_post(api, post_id):
    log.info("GET /posts/%d/comments", post_id)
    resp = api.get(f"{BASE_URL}/posts/{post_id}/comments")
    assert resp.status_code == 200
    comments = resp.json()
    assert len(comments) == 5
    for comment in comments:
        assert_schema(comment, COMMENT_SCHEMA)
        assert comment["postId"] == post_id


@pytest.mark.regression
def test_poll_comments_query_param_until_filtered(api):
    """poll_until: ?postId= query must return only that post's comments."""
    comments = poll_until(
        fn=lambda: api.get(f"{BASE_URL}/comments", params={"postId": 4}).json(),
        predicate=lambda rows: isinstance(rows, list)
        and len(rows) > 0
        and all(c["postId"] == 4 for c in rows),
        timeout=10.0, interval=1.0, desc="comments?postId=4 filtered",
    )
    for comment in comments:
        assert_schema(comment, COMMENT_SCHEMA)
