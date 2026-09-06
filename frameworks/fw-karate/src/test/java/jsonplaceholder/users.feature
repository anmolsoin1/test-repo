Feature: JSONPlaceholder users API

  Background:
    * url baseUrl

  @smoke
  Scenario: list users
    Given path 'users'
    When method get
    Then status 200
    And match response == '#[10]'
    And match response[0].username == '#string'

  @smoke
  Scenario: get user by id and check nested address
    Given path 'users', 1
    When method get
    Then status 200
    And match response.id == 1
    And match response.name == 'Leanne Graham'
    And match response.address.geo.lat == '#string'
    And match response.company.name == '#present'

  @regression
  Scenario: todos of a user
    Given path 'users', 1, 'todos'
    When method get
    Then status 200
    And match each response == { id: '#number', userId: 1, title: '#string', completed: '#boolean' }
