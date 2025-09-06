# Getting Started

This guide will help you get up and running with Hands, the agnostic test runner.

## Installation

Install Hands using pip:

```bash
pip install hands
```

## Verify Installation

Check that Hands is installed correctly:

```bash
hands --help
```

You should see the help message with available commands.

## Check Available Engines

See which test engines are available on your system:

```bash
hands list-engines
```

This will show you which engines (pytest, robot, behave) are installed and ready to use.

## Your First Test Run

### Auto-Detection

Hands can automatically detect the appropriate test engine based on your files:

```bash
# Run tests in the current directory
hands run

# Run tests in a specific folder
hands run --folder tests/
```

### Manual Engine Selection

You can also specify the engine explicitly:

```bash
# Run with pytest
hands run --engine pytest

# Run with Robot Framework
hands run --engine robot

# Run with behave
hands run --engine behave
```

### Custom Output File

Specify a custom output file:

```bash
hands run --output my_tests.xml
```

## Generating Reports

After running tests, generate HTML reports:

```bash
# Generate report from single output file
hands report output.xml

# Generate combined report from multiple files
hands report output1.xml output2.xml output3.xml --report combined.html
```

## Next Steps

- [Basic Usage Guide](user-guide/basic-usage.md)
- [Test Engine Details](user-guide/test-engines.md)
- [Examples](examples/pytest.md)
