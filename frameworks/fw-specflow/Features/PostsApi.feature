@posts
Feature: Posts API
  API-driven scenarios against jsonplaceholder.typicode.com.
  No browser involved — pure HttpClient calls from the step definitions.

  @smoke @list
  Scenario: GET posts returns 100 posts
    When I request the posts list
    Then the response status should be 200
    And the posts list should contain 100 items

  @smoke @single
  Scenario: GET single post returns the requested post
    When I request post 1
    Then the response status should be 200
    And the post should have id 1
    And the post should have userId 1

  @regression @single
  Scenario: GET another post returns correct userId
    When I request post 42
    Then the response status should be 200
    And the post should have id 42
    And the post should have userId 5
