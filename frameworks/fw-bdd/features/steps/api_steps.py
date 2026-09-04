import json

import requests
from behave import given, then, when

BASE = "https://jsonplaceholder.typicode.com"


@given("the jsonplaceholder API is reachable")
def step_reachable(context):
    r = requests.get(BASE + "/", timeout=10)
    assert r.status_code == 200, f"base URL not reachable: {r.status_code}"


@when('I GET "{path}"')
def step_get(context, path):
    context.response = requests.get(BASE + path, timeout=10)
    try:
        context.body = context.response.json()
    except json.JSONDecodeError:
        context.body = None


@when('I POST to "{path}" with title "{title}" body "{body}" userId {uid:d}')
def step_post(context, path, title, body, uid):
    context.response = requests.post(
        BASE + path,
        json={"title": title, "body": body, "userId": uid},
        timeout=10,
    )
    context.body = context.response.json()


@then("the response status is {code:d}")
def step_status(context, code):
    assert context.response.status_code == code, (
        f"expected {code}, got {context.response.status_code}"
    )


@then("the response is a JSON array of length {n:d}")
def step_array_len(context, n):
    assert isinstance(context.body, list), "response is not a JSON array"
    assert len(context.body) == n, f"expected {n} items, got {len(context.body)}"


@then('the user object has keys "id", "name", "email"')
def step_user_keys(context):
    for k in ("id", "name", "email"):
        assert k in context.body, f"missing key {k}"


@then('the user "username" is "{value}"')
def step_username(context, value):
    assert context.body.get("username") == value, (
        f"username mismatch: {context.body.get('username')}"
    )


@then('the created post has title "{title}"')
def step_post_title(context, title):
    assert context.body.get("title") == title, f"title mismatch: {context.body}"
    assert "id" in context.body, "created post has no id"


@then('every comment has "postId" equal to {pid:d}')
def step_comments_postid(context, pid):
    assert isinstance(context.body, list) and context.body, "no comments returned"
    bad = [c for c in context.body if c.get("postId") != pid]
    assert not bad, f"{len(bad)} comments with wrong postId"
