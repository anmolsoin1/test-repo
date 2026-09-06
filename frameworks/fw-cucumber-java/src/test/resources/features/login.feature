@login
Feature: Login on the-internet.herokuapp.com
  Validates the form authentication page, including data-driven
  credential combinations via a Scenario Outline examples table.

  @regression
  Scenario Outline: Login validation with multiple credential sets
    Given the login page is opened
    When the user logs in with username "<username>" and password "<password>"
    Then the login flash message contains "<message>"

    Examples:
      | username | password             | message                      |
      | tomsmith | SuperSecretPassword! | You logged into a secure area! |
      | baduser  | SuperSecretPassword! | Your username is invalid!    |
      | tomsmith | wrongpassword        | Your password is invalid!    |

  @smoke
  Scenario: Logout returns the user to the login page
    Given the login page is opened
    When the user logs in with username "tomsmith" and password "SuperSecretPassword!"
    Then the secure area heading is displayed
    When the user clicks the Logout link
    Then the login flash message contains "You logged out of the secure area!"
