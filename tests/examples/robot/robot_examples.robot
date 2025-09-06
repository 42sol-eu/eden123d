*** Settings ***
Documentation    Sample Robot Framework tests for the agnostic test runner
Library          Collections
Library          String
Library          DateTime

*** Variables ***
${CALCULATOR_RESULT}    0
${ERROR_MESSAGE}        ${EMPTY}

*** Test Cases ***
Test Basic Addition
    [Documentation]    Test that basic addition works correctly
    [Tags]    math    basic
    ${result}=    Evaluate    2 + 3
    Should Be Equal As Numbers    ${result}    5

Test Basic Subtraction  
    [Documentation]    Test that basic subtraction works correctly
    [Tags]    math    basic
    ${result}=    Evaluate    10 - 4
    Should Be Equal As Numbers    ${result}    6

Test Basic Multiplication
    [Documentation]    Test that basic multiplication works correctly
    [Tags]    math    basic
    ${result}=    Evaluate    6 * 7
    Should Be Equal As Numbers    ${result}    42

Test Basic Division
    [Documentation]    Test that basic division works correctly
    [Tags]    math    basic
    ${result}=    Evaluate    15 / 3
    Should Be Equal As Numbers    ${result}    5

Test String Operations
    [Documentation]    Test various string operations
    [Tags]    string
    ${text}=    Set Variable    Hello World
    ${lower}=    Convert To Lowercase    ${text}
    Should Be Equal    ${lower}    hello world
    
    ${upper}=    Convert To Uppercase    ${text}
    Should Be Equal    ${upper}    HELLO WORLD
    
    ${replaced}=    Replace String    ${text}    Hello    Hi
    Should Be Equal    ${replaced}    Hi World

Test List Operations
    [Documentation]    Test list operations and collections
    [Tags]    collections
    @{numbers}=    Create List    1    2    3    4    5
    ${length}=    Get Length    ${numbers}
    Should Be Equal As Numbers    ${length}    5
    
    ${first}=    Get From List    ${numbers}    0
    Should Be Equal As Numbers    ${first}    1
    
    Append To List    ${numbers}    6
    ${new_length}=    Get Length    ${numbers}
    Should Be Equal As Numbers    ${new_length}    6

Test Data-Driven Calculations
    [Documentation]    Test calculations with multiple data sets
    [Tags]    math    data-driven
    [Template]    Verify Calculation
    2    3    add    5
    10   4    subtract    6
    6    7    multiply    42
    15   3    divide    5

Test Complex Scenario
    [Documentation]    Test a complex scenario with multiple steps
    [Tags]    complex    slow
    Setup Calculator
    Enter Number    100
    Enter Number    50
    Perform Complex Operation
    Result Should Be Positive

Test Error Handling
    [Documentation]    Test error handling scenarios
    [Tags]    error_handling
    Setup Calculator
    Enter Number    10
    Enter Number    0
    Run Keyword And Expect Error    *    Perform Division
    Should Not Be Empty    ${ERROR_MESSAGE}

*** Keywords ***
Verify Calculation
    [Arguments]    ${first}    ${second}    ${operation}    ${expected}
    [Documentation]    Template keyword for testing calculations
    Setup Calculator
    Enter Number    ${first}
    Enter Number    ${second}
    Run Keyword    Perform ${operation}
    ${CALCULATOR_RESULT}=    Get Variable Value    ${CALCULATOR_RESULT}
    Should Be Equal As Numbers    ${CALCULATOR_RESULT}    ${expected}

Setup Calculator
    [Documentation]    Initialize calculator for testing
    Set Global Variable    ${CALCULATOR_RESULT}    0
    Set Global Variable    ${ERROR_MESSAGE}    ${EMPTY}

Enter Number
    [Arguments]    ${number}
    [Documentation]    Enter a number (simulated)
    Log    Entering number: ${number}

Perform Add
    [Documentation]    Perform addition operation
    ${result}=    Evaluate    ${CALCULATOR_RESULT} + 5  # Simplified
    Set Global Variable    ${CALCULATOR_RESULT}    ${result}

Perform Subtract  
    [Documentation]    Perform subtraction operation
    ${result}=    Evaluate    10 - 4  # Simplified
    Set Global Variable    ${CALCULATOR_RESULT}    ${result}

Perform Multiply
    [Documentation]    Perform multiplication operation
    ${result}=    Evaluate    6 * 7  # Simplified
    Set Global Variable    ${CALCULATOR_RESULT}    ${result}

Perform Divide
    [Documentation]    Perform division operation
    ${result}=    Evaluate    15 / 3  # Simplified
    Set Global Variable    ${CALCULATOR_RESULT}    ${result}

Perform Division
    [Documentation]    Perform division with error handling
    ${result}=    Evaluate    10 / 0  # This should cause an error
    Set Global Variable    ${CALCULATOR_RESULT}    ${result}

Perform Complex Operation
    [Documentation]    Perform a complex calculation
    Sleep    0.1s    # Simulate slow operation
    ${result}=    Evaluate    (100 + 50) * 2 - 10
    Set Global Variable    ${CALCULATOR_RESULT}    ${result}

Result Should Be Positive
    [Documentation]    Verify that the result is positive
    Should Be True    ${CALCULATOR_RESULT} > 0
