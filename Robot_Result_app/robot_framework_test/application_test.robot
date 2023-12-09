*** Settings ***
Library  SeleniumLibrary
Library  Collections
Library    OperatingSystem
Library  RequestsLibrary
Suite Setup    Open Browser To Login Page
Suite Teardown  Run Keywords    Delete User

*** Variables ***
${HOME_URL}           http://127.0.0.1:8000
# UI
${LOGIN_URL_UI}          ${HOME_URL}/accounts/login/
${REGISTER_URL_UI}       ${HOME_URL}/accounts/register/
${TEAM_CREATION_URL_UI}  ${HOME_URL}/teams/create-team/
${UPLOAD_URL_UI}         ${HOME_URL}/test-runs/create/
${TEST_RUN_URL_UI}       ${HOME_URL}/test-runs/list/
${PROFILE_URL_UI}        ${HOME_URL}/my-profile/
${LOGOUT_URL_UI}         ${HOME_URL}/accounts/logout/
# API
${TEAM_CREATION_URL_API}  ${HOME_URL}/api/v1/teams/create/
${UPLOAD_URL_API}         ${HOME_URL}/api/v1/upload/

${TOKEN_URL}          ${HOME_URL}/auth/token/login/
${USERNAME}            testuser
${EMAIL}               testuser@example.com
${PASSWORD}            password_for_testuser123
${COMMENT_TEXT}        asd
*** Test Cases ***
User Registration UI
    Create And Register User

Create Team UI
    Create Team

Upload TestRun UI
    Upload Test Run

Edit TestRun UI
    Edit Test Run To Public

Delete Team UI
    Delete Team

Fetch API Token
    Create Session    token    ${TOKEN_URL}
    &{data}=    Create Dictionary    username=${USERNAME}    password=${PASSWORD}
    ${response}=    POST On Session    token    ${TOKEN_URL}    data=${data}
    Log    Response status code: ${response.status_code}
    Log    Response body: ${response.text}
    ${auth_token}=    Evaluate    json.loads('''${response.content}''')['auth_token']    json
    Set Suite Variable    ${AUTH_TOKEN}    ${auth_token}

Create Team Using API
    Create Session    team_session    ${TEAM_CREATION_URL_API}
    ${headers}=    Create Dictionary    Authorization=Token ${AUTH_TOKEN}
    &{data}=    Create Dictionary    name=apiteam
    ${response}=    POST On Session    team_session    ${TEAM_CREATION_URL_API}    headers=${headers}    json=${data}
    Log    Response status code: ${response.status_code}
    Log    Response body: ${response.text}

    
    ${team_id}=    Evaluate    json.loads('''${response.content}''')['id']    json
    Set Suite Variable    ${API_TEAM_ID}    ${team_id}

Upload Wrong File To API
    ${absolute_file_path2} =    Get Absolute Path    ../test_data/output_1.xml
    ${response} =    Create And Send Upload Request    ${absolute_file_path2}    400

Upload Good File To API
    ${absolute_file_path3} =    Get Absolute Path    ../test_data/output_2.xml
    ${response} =    Create And Send Upload Request    ${absolute_file_path3}    201  
    ${testrun_id}=    Evaluate    json.loads('''${response.content}''')['id']    json
    Set Suite Variable    ${API_TESTRUN_ID}    ${testrun_id}

Post Comment on Testrun
    ${comment_url}=    Set Variable    ${HOME_URL}/api/v1/teams/${API_TEAM_ID}/test-runs/${API_TESTRUN_ID}/comments/
    ${headers}=        Create Dictionary    accept=application/json    Authorization=Token ${AUTH_TOKEN}    Content-Type=application/json
    &{data}=           Create Dictionary    testrun=${API_TESTRUN_ID}    text=${COMMENT_TEXT}
    ${data_json}=      Evaluate    json.dumps(${data})    json
    
    Create Session     comment_session    ${comment_url}
    ${post_response}=  POST On Session       comment_session    ${comment_url}    headers=${headers}    data=${data_json}
    Log                Response status code: ${post_response.status_code}
    Log                Response body: ${post_response.text}
    Should Be Equal As Numbers    ${post_response.status_code}    201

    ${get_response}=   GET On Session         comment_session    ${comment_url}    headers=${headers}
    Log                Response status code: ${get_response.status_code}
    Log                Response body: ${get_response.text}
    ${response_body}=  Evaluate            json.loads('''${get_response.content}''')    json
    Should Be Equal As Strings    ${response_body['results'][0]['text']}    ${COMMENT_TEXT}

Access Admin Functions Without Admin Rights
    ${headers}=    Create Dictionary    Authorization=Token ${AUTH_TOKEN}    Content-Type=application/json
    &{data}=       Create Dictionary    key_name=name
    ${data_json}=  Evaluate    json.dumps(${data})    json

    Create Session     api_session    ${HOME_URL}/attributes/create/
    ${response}=       POST On Session   api_session    ${HOME_URL}/attributes/create/    headers=${headers}    data=${data_json}    expected_status=403
    Log                Response status code: ${response.status_code}
    Log                Response body: ${response.text}

*** Keywords ***

Get Absolute Path
    [Arguments]    ${relative_path}
    ${absolute_path}=    Join Path    ${CURDIR}    ${relative_path}
    [Return]    ${absolute_path}

Create And Send Upload Request
    [Arguments]    ${file_path}    ${expected_status}
    Create Session    upload_session    ${UPLOAD_URL_API}
    ${headers}=    Create Dictionary    accept=application/json    Authorization=Token ${AUTH_TOKEN}

    ${file}=    Get Binary File    ${file_path}
    ${files}=    Create Dictionary    output_file=${file_path}    output_file=${file}    type=text/xml
    ${data}=    Create Dictionary    team=${API_TEAM_ID}    attributes={}
    
    ${response}=    POST On Session    upload_session    ${UPLOAD_URL_API}    headers=${headers}    files=${files}    data=${data}     expected_status=${expected_status}
    Log    Response status code: ${response.status_code}
    Log    Response body: ${response.text}
    Should Be Equal As Numbers    ${response.status_code}    ${expected_status}

    [Return]    ${response}

Get Binary File
    [Arguments]    ${file_path}
    ${file}=    Get File    ${file_path}
    [Return]    ${file}

Open Browser To Login Page
    Open Browser    ${LOGIN_URL_UI}    browser=Chrome
    Maximize Browser Window

Create And Register User
    Go To  ${REGISTER_URL_UI}
    Wait Until Element Is Visible  id:floatingUsername
    Input Text  id:floatingUsername  ${USERNAME}
    Input Text  id:floatingEmail  ${EMAIL}
    Input Text  id:floatingFirstName  UserFirstName
    Input Text  id:floatingLastName  UserLastName
    Input Text  id:floatingPassword1  ${PASSWORD}
    Input Text  id:floatingPassword2  ${PASSWORD}
    Click Button  xpath://button[@type='submit']

Create Team
    Go To  ${TEAM_CREATION_URL_UI}
    Wait Until Element Is Visible    id:teamName 
    Input Text  id:teamName  RobotFrameworkTestTeam
    Click Button  xpath://button[@type='submit']

Upload Test Run
    Go To  ${UPLOAD_URL_UI}

    Wait Until Element Is Visible    id:teamDropdown 

    Click Element    id=teamDropdown
    Wait Until Element Is Visible    id=filter
    Input Text    id=filter    RobotFrameworkTestTeam
    Wait Until Element Is Visible    //li[contains(text(),'RobotFrameworkTestTeam')]
    Click Element    //li[contains(text(),'RobotFrameworkTestTeam')]

    ${absolute_file_path} =    Get Absolute Path    ../test_data/output_2.xml

    Choose File    id=outputFile    ${absolute_file_path}
    Click Element    //button[contains(text(),'Upload Test Run')]

    Wait Until Element Is Visible    //div[contains(text(),'Upload Successfull')]
    Element Should Contain    //div[contains(text(),'Upload Successfull')]    Upload Successfull

Edit Test Run To Public
    Go To  ${TEST_RUN_URL_UI}

    Wait Until Element Is Visible    id:teamDropdown 

    Click Element    id=teamDropdown
    Wait Until Element Is Visible    id=filter
    Input Text    id=filter    RobotFrameworkTestTeam
    Wait Until Element Is Visible    //li[contains(text(),'RobotFrameworkTestTeam')]
    Click Element    //li[contains(text(),'RobotFrameworkTestTeam')]


    Wait Until Element Is Visible  css:.card
    Click Element  id:testrun0

    Wait Until Element Is Visible    id=testrundetails
    Click Element  id:testrundetails

    Click Element  id:editbutton
    Click Element  id:public_testrun
    Click Element  id:editbutton
    
    Go To  ${TEST_RUN_URL_UI}

    Wait Until Element Is Visible    id:teamDropdown 

    Click Element    id=teamDropdown
    Wait Until Element Is Visible    id=filter
    Input Text    id=filter    RobotFrameworkTestTeam
    Wait Until Element Is Visible    //li[contains(text(),'RobotFrameworkTestTeam')]
    Click Element    //li[contains(text(),'RobotFrameworkTestTeam')]


    Wait Until Element Is Visible  id=is_public  5s


Delete Team
    Go To  ${HOME_URL}/teams/list/

    Wait Until Element Is Visible    //p[contains(text(), ${USERNAME})]
    Click Element    //p[contains(text(), ${USERNAME})]

    Wait Until Element Is Visible    id=delete_team_button
    Click Element  id:delete_team_button

    Go To  ${HOME_URL}/teams/list/
    Wait Until Element Is Not Visible    //p[contains(text(), ${USERNAME})]    5s

Delete User
    Go To  ${PROFILE_URL_UI}

    Wait Until Element Is Visible    id=editProfile
    Click Element    id:editProfile
    Wait Until Element Is Visible    id=delProf
    Click Element  id:delProf
    Wait Until Element Is Visible    id=delProfConfirm
    Click Element  id:delProfConfirm

    Try Login
    Close Browser


Try Login
    Go To  ${LOGIN_URL_UI}

    Input Text  id:floatingUsername  ${USERNAME}
    Input Text  id:floatingPassword  ${PASSWORD}
    Click Button  xpath://button[@type='submit']
    Wait Until Element Is Visible    //li[contains(text(), 'Please enter a correct')]    5s
    
