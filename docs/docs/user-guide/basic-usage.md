# Basic Usage

This guide covers the basic usage patterns for the Hands test runner.

## Running Tests

### Auto-Detection Mode

The simplest way to run tests is to let Hands auto-detect the appropriate engine:

```bash
# Run tests in current directory
hands run

# Run tests in specific folder
hands run --folder tests/
```

Hands will automatically detect the engine based on:

1. **File extensions**: `.feature` for behave, `.robot` for Robot Framework, `test_*.py` for pytest
2. **Directory structure**: `features/` folder for behave, common pytest patterns
3. **Installed packages**: Falls back to checking what's installed

### Manual Engine Selection

You can explicitly specify which engine to use:

```bash
# Force pytest
hands run --engine pytest --folder tests/

# Force Robot Framework  
hands run --engine robot --folder robot_tests/

# Force behave
hands run --engine behave --folder features/
```

### Output Configuration

Control where test results are saved:

```bash
# Custom output file
hands run --output my_results.xml

# Verbose output
hands run --verbose

# Combination
hands run --engine pytest --folder tests/ --output pytest_results.xml --verbose
```

### Pass-Through Arguments

You can pass additional arguments directly to the underlying test engine:

```bash
# Pytest arguments
hands run --engine pytest tests/ -- --maxfail=3 --tb=short

# Robot Framework arguments  
hands run --engine robot robot_tests/ -- --include smoke

# Behave arguments
hands run --engine behave features/ -- --tags=@critical
```

## Generating Reports

### Single Report

Generate an HTML report from a single test run:

```bash
hands report output.xml
```

This creates `report.html` and `log.html` in the current directory.

### Combined Reports

Combine results from multiple test runs:

```bash
# Run different engines
hands run --engine pytest --output pytest.xml
hands run --engine robot --output robot.xml  
hands run --engine behave --output behave.xml

# Generate combined report
hands report pytest.xml robot.xml behave.xml --report combined.html
```

### Custom Report Names

```bash
hands report output.xml --report my_report.html --log my_log.html
```

## Engine Status

Check which test engines are available:

```bash
hands list-engines
```

This shows:
- ✓ Available engines (installed and ready)
- ✗ Unavailable engines (not installed or misconfigured)

## Common Workflows

### CI/CD Pipeline

```bash
#!/bin/bash
# Run all test types and generate combined report

# Run pytest tests
hands run --engine pytest tests/ --output pytest.xml

# Run Robot Framework tests  
hands run --engine robot robot_tests/ --output robot.xml

# Run behave tests
hands run --engine behave features/ --output behave.xml

# Generate combined report
hands report pytest.xml robot.xml behave.xml --report final_report.html

echo "All tests completed. Report: final_report.html"
```

### Development Workflow

```bash
# Quick test run (auto-detect)
hands run

# Test specific component
hands run --folder tests/unit/

# Verbose output for debugging
hands run --verbose --folder tests/integration/
```
