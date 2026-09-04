*** Settings ***
Documentation     Regression suite: deeper keyword-driven checks on jsonplaceholder.
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}       https://jsonplaceholder.typicode.com

*** Test Cases ***
Create Post Returns 201 And Echoes Payload
    [Tags]    regression
    [Documentation]    POST /posts echoes back title/body/userId.
    &{payload}=    Create Dictionary    title=he-robot    body=playground    userId=${1}
    ${response}=    POST    ${BASE_URL}/posts    json=${payload}    expected_status=201
    ${body}=    Set Variable    ${response.json()}
    Should Be Equal    ${body["title"]}    he-robot

Users Endpoint Returns Ten Users
    [Tags]    regression
    [Documentation]    GET /users returns exactly 10 users.
    ${response}=    GET    ${BASE_URL}/users    expected_status=200
    ${count}=    Get Length    ${response.json()}
    Should Be Equal As Integers    ${count}    10

First User Has A Company Name
    [Tags]    regression    smoke
    [Documentation]    Users[0] has nested company.name (tagged smoke too, to demo tag overlap).
    ${response}=    GET    ${BASE_URL}/users/1    expected_status=200
    ${user}=    Set Variable    ${response.json()}
    Dictionary Should Contain Key    ${user["company"]}    name
