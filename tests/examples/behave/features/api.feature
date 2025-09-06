Feature: User Management API
  As an API user
  I want to manage user accounts
  So that I can create and retrieve user information

  Background:
    Given I have an API client
    And I am authenticated as "admin" with password "secret"

  Scenario: Create a new user
    When I create a user with name "John Smith" and email "john@example.com"
    Then the user should be created successfully
    And the response should contain user ID

  Scenario: Retrieve an existing user
    When I request user with ID 1
    Then I should get user information
    And the user name should be "John Doe"

  Scenario: Handle non-existent user
    When I request user with ID 999
    Then I should get a "not found" error

  Scenario: Handle unauthorized access
    Given I am not authenticated
    When I request user with ID 1
    Then I should get an "unauthorized" error

  @validation
  Scenario Outline: User creation validation
    When I create a user with name "<name>" and email "<email>"
    Then the response status should be <status>

    Examples:
      | name       | email              | status |
      | John Doe   | john@example.com   | 201    |
      | Jane Smith | jane@example.com   | 201    |
      |            | missing@name.com   | 400    |
      | Missing    |                    | 400    |
