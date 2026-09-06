Feature: JSONPlaceholder posts API

  Background:
    * url baseUrl

  @smoke
  Scenario: get all posts returns 100 items
    Given path 'posts'
    When method get
    Then status 200
    And match response == '#[100]'
    And match response[0].id == 1

  @smoke @regression
  Scenario: get single post by id
    Given path 'posts', 1
    When method get
    Then status 200
    And match response.id == 1
    And match response.userId == '#number'
    And match response.title == '#string'
    And match response.body == '#present'

  @regression
  Scenario: create a post and verify echo
    Given path 'posts'
    And request { title: 'fw-karate', body: 'matrix post', userId: 42 }
    When method post
    Then status 201
    And match response.title == 'fw-karate'
    And match response.userId == 42
    And match response.id == '#number'

  @regression
  Scenario: comments of a post are well-formed
    Given path 'posts', 1, 'comments'
    When method get
    Then status 200
    And match each response == { id: '#number', postId: 1, name: '#string', email: '#string', body: '#string' }

  @regression
  Scenario: DELIBERATE FAILURE - wrong status expected for missing post
    Given path 'posts', 99999
    When method get
    Then status 200
