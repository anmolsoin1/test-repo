import logging

import pytest

from conftest import BASE_URL

log = logging.getLogger("he-pytest.comments")


@pytest.mark.smoke
def test_get_all_comments(api):
    log.info("GET /comments")
    resp = api.get(f"{BASE_URL}/comments")
    assert resp.status_code == 200
    assert len(resp.json()) == 500


@pytest.mark.regression
def test_comments_for_post(api):
    log.info("GET /posts/1/comments")
    resp = api.get(f"{BASE_URL}/posts/1/comments")
    assert resp.status_code == 200
    comments = resp.json()
    assert len(comments) == 5
    assert all(c["postId"] == 1 for c in comments)


@pytest.mark.regression
def test_comment_has_email(api):
    log.info("GET /comments/1")
    resp = api.get(f"{BASE_URL}/comments/1")
    assert resp.status_code == 200
    comment = resp.json()
    assert "@" in comment["email"]
