# Test Engines

Hands supports three different test engines, each with its own strengths and use cases.

## Pytest

Pytest is a mature testing framework for Python with extensive plugin ecosystem.

### Features
- Fixtures for test setup and teardown
- Parametrized testing
- Marking tests with custom tags
- Rich assertion introspection
- Plugin ecosystem

### Usage with Hands

```bash
# Auto-detected for files matching test_*.py pattern
hands run --folder tests/

# Explicit engine selection
hands run --engine pytest --folder tests/

# With pytest arguments
hands run --engine pytest tests/ -- --maxfail=3 --tb=short -v
```

### Robot XML Output

Hands includes a pytest plugin that automatically generates Robot Framework-compatible XML output. The plugin is automatically activated when using Hands.

Configuration options:
- `--robot-output`: Output XML file path (default: `output.xml`)
- `--robot-suite-name`: Suite name in XML (default: `Pytest Suite`)

## Robot Framework

Robot Framework is a keyword-driven testing framework with human-readable syntax.

### Features
- Keyword-driven testing
- Built-in test libraries
- Custom keyword creation
- Rich reporting
- Test data driven approach

### Usage with Hands

```bash
# Auto-detected for .robot files
hands run --folder robot_tests/

# Explicit engine selection  
hands run --engine robot --folder robot_tests/

# With Robot Framework arguments
hands run --engine robot robot_tests/ -- --include smoke --loglevel DEBUG
```

### Supported Formats

1. **Robot Files (.robot)**: Standard Robot Framework syntax
2. **Python Libraries**: Custom keyword libraries written in Python

Example Robot file:
```robotframework
*** Test Cases ***
Test Calculator Addition
    ${result}=    Evaluate    2 + 3
    Should Be Equal As Numbers    ${result}    5
```

Example Python library:
```python
from robot.api.deco import keyword, library

@library
class CalculatorLibrary:
    @keyword
    def add_numbers(self, a, b):
        return float(a) + float(b)
```

## Behave

Behave is a BDD (Behavior Driven Development) framework using Gherkin syntax.

### Features
- Gherkin syntax (Given/When/Then)
- Scenario outlines for data-driven tests
- Tags for test organization
- Hooks for setup/teardown
- Natural language test descriptions

### Usage with Hands

```bash
# Auto-detected for .feature files
hands run --folder features/

# Explicit engine selection
hands run --engine behave --folder features/

# With behave arguments  
hands run --engine behave features/ -- --tags=@smoke --verbose
```

### Directory Structure

Behave requires a specific directory structure:

```
project/
├── features/
│   ├── calculator.feature
│   └── api.feature
└── steps/
    ├── calculator_steps.py
    └── api_steps.py
```

### Robot XML Output

Hands includes a custom behave formatter that generates Robot Framework-compatible XML. This formatter is automatically used when running behave through Hands.

Example feature file:
```gherkin
Feature: Calculator Operations
  Scenario: Addition
    Given I have a calculator
    When I add 2 and 3
    Then the result should be 5
```

Example step definition:
```python
from behave import given, when, then

@given('I have a calculator')
def step_impl(context):
    context.calculator = Calculator()

@when('I add {a:d} and {b:d}')
def step_impl(context, a, b):
    context.result = context.calculator.add(a, b)

@then('the result should be {expected:d}')
def step_impl(context, expected):
    assert context.result == expected
```

## Engine Selection Strategy

Hands uses the following strategy to auto-detect the appropriate engine:

1. **File Extensions**:
   - `.feature` files → behave
   - `.robot` files → Robot Framework
   - `test_*.py` files → pytest

2. **Directory Structure**:
   - `features/` directory → behave
   - `tests/` with Python files → pytest
   - Any `.robot` files → Robot Framework

3. **Fallback to Installed Packages**:
   - Check for pytest, then Robot Framework, then behave

You can always override auto-detection using the `--engine` parameter.
