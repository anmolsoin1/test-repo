@users
Feature: Users API
  Second feature file so discovery has multiple items to split.

  @smoke @list
  Scenario: GET users returns 10 users
    When I request the users list
    Then the response status should be 200
    And the users list should contain 10 items

  @regression @single
  Scenario: GET single user has expected username
    When I request user 3
    Then the response status should be 200
    And the user should have username "Samantha"

  @regression @deliberate-failure
  Scenario: DELIBERATE FAILURE - existing post wrongly expected to be missing
    When I request post 5
    Then the response status should be 404
