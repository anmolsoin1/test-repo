*** Settings ***
Documentation     Smoke suite: keyword-driven checks against jsonplaceholder.
Library           RequestsLibrary
Library           Collections

*** Variables ***
${BASE_URL}       https://jsonplaceholder.typicode.com

*** Test Cases ***
Get Posts Returns List
    [Tags]    smoke
    [Documentation]    GET /posts returns a non-empty list of posts.
    ${posts}=    Fetch Resource    /posts
    ${count}=    Get Length    ${posts}
    Should Be True    ${count} > 0

Get Single Post Has Expected Fields
    [Tags]    smoke
    [Documentation]    GET /posts/1 contains id, title and body.
    ${post}=    Fetch Resource    /posts/1
    Dictionary Should Contain Key    ${post}    id
    Dictionary Should Contain Key    ${post}    title
    Dictionary Should Contain Key    ${post}    body

*** Keywords ***
Fetch Resource
    [Arguments]    ${path}
    ${response}=    GET    ${BASE_URL}${path}    expected_status=200
    [Return]    ${response.json()}
