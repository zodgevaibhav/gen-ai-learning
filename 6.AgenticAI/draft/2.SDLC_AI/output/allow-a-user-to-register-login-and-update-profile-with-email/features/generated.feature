```gherkin
# file: features/user_registration.feature

Feature: User Registration
  As a user
  I want to register an account
  So that I can log in and update my profile

  Background:
    Given the application is running

  Scenario: Successful user registration
    When the user registers with valid email and password
    Then the user should receive a verification email
    And the user should be redirected to the login page

  Scenario: Registration with an already registered email
    When the user registers with an email that is already in use
    Then the user should see an error message indicating the email is already registered

  Scenario: Registration with invalid email format
    When the user registers with an invalid email format
    Then the user should see an error message indicating the email format is invalid

  Scenario: Registration with weak password
    When the user registers with a password that does not meet security requirements
    Then the user should see an error message indicating the password is too weak

  Scenario: Rate limiting on registration attempts
    Given the user has attempted to register 5 times in a minute
    When the user attempts to register again
    Then the user should see a message indicating too many registration attempts

# file: features/user_login.feature

Feature: User Login
  As a user
  I want to log in to my account
  So that I can access my profile

  Background:
    Given the application is running

  Scenario: Successful login
    Given the user has a registered account
    When the user logs in with valid credentials
    Then the user should be redirected to their profile page

  Scenario: Login with unregistered email
    When the user logs in with an email that is not registered
    Then the user should see an error message indicating the email is not found

  Scenario: Login with incorrect password
    Given the user has a registered account
    When the user logs in with the correct email but incorrect password
    Then the user should see an error message indicating the password is incorrect

  Scenario: Rate limiting on login attempts
    Given the user has attempted to log in 5 times in a minute
    When the user attempts to log in again
    Then the user should see a message indicating too many login attempts

# file: features/user_profile_update.feature

Feature: User Profile Update
  As a user
  I want to update my profile information
  So that my account details are current

  Background:
    Given the application is running
    And the user is logged in

  Scenario: Successful profile update
    When the user updates their profile with valid information
    Then the user should see a success message
    And the profile should reflect the updated information

  Scenario: Profile update with invalid email format
    When the user updates their profile with an invalid email format
    Then the user should see an error message indicating the email format is invalid

  Scenario: Profile update with weak password
    When the user updates their password to a weak password
    Then the user should see an error message indicating the password is too weak

  Scenario: Profile update without required fields
    When the user attempts to update their profile without filling in required fields
    Then the user should see an error message indicating the required fields are missing

  Scenario: Concurrent profile updates
    Given the user has initiated a profile update
    And another process attempts to update the same profile
    Then the user should see a message indicating the profile is being updated by another process

  Scenario: Performance of profile update
    When the user updates their profile
    Then the update should complete within 2 seconds
```