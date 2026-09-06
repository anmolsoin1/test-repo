@checkbox
Feature: Checkboxes on the-internet.herokuapp.com
  Exercises checkbox toggling with a mix of locator strategies
  and explicit waits.

  @smoke
  Scenario: First checkbox can be checked
    Given the checkboxes page is opened
    When the user checks the first checkbox
    Then the first checkbox is selected

  @regression
  Scenario: Both checkboxes toggle independently
    Given the checkboxes page is opened
    Then the second checkbox is selected by default
    When the user checks the first checkbox
    And the user unchecks the second checkbox
    Then the first checkbox is selected
    And the second checkbox is not selected

  @deliberate-failure
  Scenario: DELIBERATE FAILURE - nonexistent promo banner is expected
    Given the checkboxes page is opened
    Then the promo banner with id "nonexistent-banner" is displayed
