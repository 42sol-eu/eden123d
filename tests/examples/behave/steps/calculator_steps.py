"""Step definitions for calculator feature tests."""
from behave import given, when, then
import time


class Calculator:
    """Simple calculator class for testing."""
    
    def __init__(self):
        self.first_number = 0
        self.second_number = 0
        self.result = 0
        self.error_message = None
    
    def add(self):
        self.result = self.first_number + self.second_number
    
    def subtract(self):
        self.result = self.first_number - self.second_number
    
    def multiply(self):
        self.result = self.first_number * self.second_number
    
    def divide(self):
        if self.second_number == 0:
            self.error_message = "Division by zero error"
        else:
            self.result = self.first_number / self.second_number


@given('I have a calculator')
def step_have_calculator(context):
    """Initialize calculator."""
    context.calculator = Calculator()


@given('I enter the number {number:d}')
def step_enter_number(context, number):
    """Enter a number into the calculator."""
    if not hasattr(context.calculator, 'first_number') or context.calculator.first_number == 0:
        context.calculator.first_number = number
    else:
        context.calculator.second_number = number


@when('I press the add button')
def step_press_add(context):
    """Press the add button."""
    context.calculator.add()


@when('I press the subtract button')
def step_press_subtract(context):
    """Press the subtract button."""
    context.calculator.subtract()


@when('I press the multiply button')
def step_press_multiply(context):
    """Press the multiply button."""
    context.calculator.multiply()


@when('I press the divide button')
def step_press_divide(context):
    """Press the divide button."""
    context.calculator.divide()


@when('I perform a complex calculation')
def step_complex_calculation(context):
    """Perform a complex calculation (simulates slow operation)."""
    time.sleep(0.1)  # Simulate slow operation
    # Complex calculation: (first + second) * 2 - 10
    context.calculator.result = (context.calculator.first_number + context.calculator.second_number) * 2 - 10


@then('the result should be {expected_result:d}')
def step_result_should_be(context, expected_result):
    """Check that the result matches expected value."""
    assert context.calculator.result == expected_result, \
        f"Expected {expected_result}, but got {context.calculator.result}"


@then('the result should be positive')
def step_result_positive(context):
    """Check that the result is positive."""
    assert context.calculator.result > 0, \
        f"Expected positive result, but got {context.calculator.result}"


@then('I should see an error message')
def step_see_error_message(context):
    """Check that an error message is displayed."""
    assert context.calculator.error_message is not None, \
        "Expected an error message, but none was found"
