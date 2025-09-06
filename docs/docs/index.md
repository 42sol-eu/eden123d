# Hands - Agnostic Test Runner

Hands is a reliable agnostic test runner that can execute tests written for Robot Framework, pytest, and behave while generating consistent Robot Framework-compatible output.xml files.

## Key Features

- **Multi-Engine Support**: Run tests with pytest, Robot Framework, or behave
- **Auto-Detection**: Automatically detects the appropriate test engine based on file patterns
- **Unified Output**: All engines generate Robot Framework-compatible XML output
- **Combined Reporting**: Use Robot Framework's rebot to create unified HTML reports
- **CLI Interface**: Simple command-line interface with pass-through arguments

## Quick Start

### Installation

```bash
pip install hands
```

### Run Tests

```bash
# Auto-detect and run tests in current directory
hands run

# Specify engine explicitly
hands run --engine pytest tests/

# Generate combined report
hands report output.xml --report combined_report.html
```

## Supported Test Engines

### Pytest
- Uses pytest plugin to generate Robot XML output
- Supports all pytest features including fixtures, parametrization, and markers
- Pass-through arguments to pytest

### Robot Framework
- Native Robot Framework execution
- Supports both .robot files and Python-based test libraries
- Direct output.xml generation

### Behave
- BDD-style testing with Gherkin syntax
- Custom formatter generates Robot XML output
- Supports tags, scenario outlines, and hooks

## Architecture

The tool uses an object-oriented architecture with:

- **Engine Detection**: Automatic detection of appropriate test engine
- **Test Engine Classes**: Separate implementations for each test framework
- **Unified XML Output**: Common Robot Framework XML format
- **CLI Interface**: Typer-based command-line interface

## Next Steps

- [Getting Started Guide](getting-started.md)
- [Installation Instructions](user-guide/installation.md)
- [Basic Usage Examples](user-guide/basic-usage.md)
