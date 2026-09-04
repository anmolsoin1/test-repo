Feature: Posts API on jsonplaceholder
  Read checks plus one POST against /posts.

  @smoke
  Scenario: Posts list returns 100 posts
    Given the jsonplaceholder API is reachable
    When I GET "/posts"
    Then the response status is 200
    And the response is a JSON array of length 100

  @regression
  Scenario: Create a post returns 201 with echoed body
    Given the jsonplaceholder API is reachable
    When I POST to "/posts" with title "he-bdd" body "hello" userId 1
    Then the response status is 201
    And the created post has title "he-bdd"

  @regression
  Scenario: Comments for post 1 are scoped correctly
    Given the jsonplaceholder API is reachable
    When I GET "/posts/1/comments"
    Then the response status is 200
    And every comment has "postId" equal to 1
