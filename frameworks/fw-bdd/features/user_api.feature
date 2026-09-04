Feature: Users API on jsonplaceholder
  Basic CRUD-ish reads against the jsonplaceholder /users endpoint.

  @smoke
  Scenario: Users list returns 10 users
    Given the jsonplaceholder API is reachable
    When I GET "/users"
    Then the response status is 200
    And the response is a JSON array of length 10

  @smoke
  Scenario: Single user has expected shape
    Given the jsonplaceholder API is reachable
    When I GET "/users/1"
    Then the response status is 200
    And the user object has keys "id", "name", "email"
    And the user "username" is "Bret"

  @regression
  Scenario: Unknown user returns 404
    Given the jsonplaceholder API is reachable
    When I GET "/users/9999"
    Then the response status is 404
