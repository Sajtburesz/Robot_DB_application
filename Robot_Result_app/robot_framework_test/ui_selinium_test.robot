*** Settings ***
Library  SeleniumLibrary
Suite Setup    Open Browser To Login Page
Suite Teardown  Close Browser

*** Variables ***
${HOME_URL}           http://127.0.0.1:8000
${LOGIN_URL}          ${HOME_URL}/accounts/login/
${REGISTER_URL}       ${HOME_URL}/accounts/register/
${TEAM_CREATION_URL}  ${HOME_URL}/teams/create-team/
${UPLOAD_URL}         ${HOME_URL}/test-runs/create/
${TEST_RUN_URL}       ${HOME_URL}/test-runs/list/
${PROFILE_URL}        ${HOME_URL}/my-profile/
${LOGOUT_URL}         ${HOME_URL}/accounts/logout/
${USERNAME}            testuser
${EMAIL}               testuser@example.com
${PASSWORD}            password_for_testuser123

*** Test Cases ***
User Registration to Test Run Management
    Create And Register User
    Create Team
    Upload Test Run
    # Edit Test Run To Public
    # Delete Test Run
    # Delete Team
    # Delete User

*** Keywords ***
Open Browser To Login Page
    Open Browser    ${LOGIN_URL}    browser=Chrome
    Maximize Browser Window

Create And Register User
    Go To  ${REGISTER_URL}
    Wait Until Element Is Visible  id:floatingUsername
    Input Text  id:floatingUsername  ${USERNAME}
    Input Text  id:floatingEmail  ${EMAIL}
    Input Text  id:floatingFirstName  UserFirstName
    Input Text  id:floatingLastName  UserLastName
    Input Text  id:floatingPassword1  ${PASSWORD}
    Input Text  id:floatingPassword2  ${PASSWORD}
    Click Button  xpath://button[@type='submit']

Create Team
    Go To  ${TEAM_CREATION_URL}
    Input Text  id:teamName  RobotFrameworkTestTeam
    Click Button  xpath://button[@type='submit']
    # Wait Until Element Is Visible  team_created_success_message

Upload Test Run
    Go To  ${UPLOAD_URL}
    Select From List By Label  teamDropdown  RobotFrameworkTestTeam
    Choose File  id:outputFile  test_data/output_2.xml
    Click Button  xpath://button[@type='submit']
    # Wait Until Element Is Visible  upload_success_message

Edit Test Run To Public
    Click Element  edit_test_run_button
    Select Checkbox  public_checkbox
    Click Button  save_button
    Wait Until Element Is Visible  edit_success_message

# Delete Test Run
#     Click Element  delete_test_run_button
#     Confirm Action  # Implement a keyword to handle confirmation dialogs

# Delete Team
#     Go To  ${HOME_URL}/teams
#     Click Element  delete_team_button
#     Confirm Action  # Implement a keyword to handle confirmation dialogs

# Delete User
#     Go To  ${PROFILE_URL}
#     Click Element  delete_user_button
#     Confirm Action  # Implement a keyword to handle confirmation dialogs

# Confirm Action
#     [Arguments]  ${confirmation_element}
#     Wait Until Element Is Visible  ${confirmation_element}
#     Click Button  confirm_button
