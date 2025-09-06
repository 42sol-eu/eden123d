Feature: Calculator Operations
    As a user
    I want to perform basic calculator operations
    So that I can compute mathematical results

    Background:
        Given I have a calculator

    Scenario: Addition of two numbers
        Given I enter the number 5
        And I enter the number 3
        When I press the add button
        Then the result should be 8

    Scenario: Subtraction of two numbers
        Given I enter the number 10
        And I enter the number 4
        When I press the subtract button
        Then the result should be 6

    Scenario: Multiplication of two numbers
        Given I enter the number 6
        And I enter the number 7
        When I press the multiply button
        Then the result should be 42

    Scenario: Division of two numbers
        Given I enter the number 15
        And I enter the number 3
        When I press the divide button
        Then the result should be 5

    Scenario Outline: Multiple calculations
        Given I enter the number <first>
        And I enter the number <second>
        When I press the <operation> button
        Then the result should be <result>

        Examples:
            | first | second | operation | result |
            | 2     | 3      | add       | 5      |
            | 10    | 2      | subtract  | 8      |
            | 4     | 5      | multiply  | 20     |
            | 12    | 3      | divide    | 4      |

    @slow
    Scenario: Complex calculation
        Given I enter the number 100
        And I enter the number 50
        When I perform a complex calculation
        Then the result should be positive

    @error_handling
    Scenario: Division by zero
        Given I enter the number 10
        And I enter the number 0
        When I press the divide button
        Then I should see an error message
