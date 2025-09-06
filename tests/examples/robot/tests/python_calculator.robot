*** Settings ***
Documentation    Python-based Robot Framework tests using custom library
Library          CalculatorLibrary
Library          Collections

*** Test Cases ***
Test Addition With Custom Library
    [Documentation]    Test addition using Python library
    [Tags]    python    calculator
    Reset Calculator
    ${result}=    Add Numbers    5    3
    Result Should Be    8
    ${last_result}=    Get Last Result
    Should Be Equal As Numbers    ${last_result}    8

Test Subtraction With Custom Library
    [Documentation]    Test subtraction using Python library
    [Tags]    python    calculator
    Reset Calculator
    ${result}=    Subtract Numbers    10    4
    Result Should Be    6

Test Multiplication With Custom Library
    [Documentation]    Test multiplication using Python library
    [Tags]    python    calculator
    Reset Calculator
    ${result}=    Multiply Numbers    6    7
    Result Should Be    42

Test Division With Custom Library
    [Documentation]    Test division using Python library
    [Tags]    python    calculator
    Reset Calculator
    ${result}=    Divide Numbers    15    3
    Result Should Be    5

Test Division By Zero Error
    [Documentation]    Test that division by zero raises an error
    [Tags]    python    calculator    error
    Reset Calculator
    Run Keyword And Expect Error    ValueError: Cannot divide by zero
    ...    Divide Numbers    10    0

*** Keywords ***
Test Setup
    [Documentation]    Setup for each test
    Reset Calculator

Test Teardown
    [Documentation]    Cleanup after each test
    Reset Calculator
