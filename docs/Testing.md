# Testing Guide for Caracterizar Project

This document outlines the testing procedures, environment setup, and execution instructions for the Caracterizar Python project.

## Overview

The project includes a comprehensive test suite designed to verify the functionality of various components, with particular focus on the unified measurement results saving system. This guide explains how to set up the testing environment and execute tests effectively.

## Test Suite Structure

The test suite is organized in the `tests/` directory:

```
tests/
├── __init__.py
├── conftest.py
├── test_common_save_results.py      # Tests for unified save functionality
├── test_config.py                   # Configuration parsing tests
├── test_config_functions.py         # Configuration utility function tests
├── test_result_file.py              # Result file handling tests
├── test_statistics.py               # Statistical calculation tests
├── test_wafermap_file.py            # Wafer map file parsing tests
└── fixtures/
    ├── test_result.dat              # Sample result data file
    ├── test_wafermap.ppg            # Sample wafer map file
    └── sample_result.dat            # Additional sample data
```

### New Test Suite: `test_common_save_results.py`

This test file specifically validates the unified measurement results saving functionality implemented in `config/default/tests/common.py`. It tests:

- `build_results_folder()`: Constructs standardized folder paths
- `get_output_separator()`: Converts separator strings to actual characters
- `save_results_to_file()`: Saves measurement data in columnated text format

## Environment Setup

### Prerequisites

1. Python 3.7+ installed
2. Git (for version control)

### Development Dependencies

Install the required development dependencies:

```bash
pip install -r requirements_dev.txt
```

The `requirements_dev.txt` file contains:
```
pytest>=6.0
pytest-mock>=3.0
```

### Environment Variables

No special environment variables are required for running the tests. However, ensure you're running from the project root directory where `requirements_dev.txt` is located.

## Running Tests

### From Project Root

To execute the complete test suite:

```bash
python -m pytest tests/
```

### With Verbose Output

For detailed test information:

```bash
python -m pytest tests/ -v
```

### Running Specific Test Files

To run only the new save results tests:

```bash
python -m pytest tests/test_common_save_results.py -v
```

To run tests for a specific module:

```bash
python -m pytest tests/test_statistics.py -v
```

### Generating Coverage Reports

To see what percentage of code is covered by tests:

```bash
python -m pytest tests/ --cov=config --cov-report=html
```

This will generate an HTML coverage report in the `htmlcov/` directory.

## Test Execution Details

### Test Discovery

Pytest automatically discovers test files and functions:
- Files matching `test_*.py` or `*_test.py`
- Functions matching `test_*`

### Test Isolation

Each test function runs in isolation:
- Temporary directories are used for file operations
- Mock objects simulate the main application interface
- No permanent changes are made to the filesystem
- State is not shared between tests

### Test Output Interpretation

- `.` - Test passed
- `F` - Test failed
- `E` - Error occurred during test collection/setup
- `s` - Test skipped
- `x` - Test failed but was expected to fail (xfail)
- `X` - Test passed but was expected to fail (xpass)

## Test Suite Coverage

### Common Save Results Tests (`test_common_save_results.py`)

| Test Function | Purpose |
|---------------|---------|
| `test_build_results_folder` | Verifies folder path construction with correct wafer number zero-padding |
| `test_get_output_separator` | Tests conversion of separator strings to actual characters (space, tab, comma) |
| `test_save_results_to_file_basic` | Tests saving multi-row data with prefix and suffix in filename |
| `test_save_results_to_file_single_row` | Tests handling of single-row data arrays |
| `test_save_results_to_file_space_separator` | Validates space-separated output format |
| `test_save_results_to_file_creates_directories` | Ensures automatic creation of directory structure |
| `test_save_results_to_file_default_parameters` | Tests minimal parameter usage with defaults |

### Existing Test Suites

| Test File | Purpose |
|-----------|---------|
| `test_statistics.py` | Tests statistical calculation functions in `modules/statistics_estepa.py` |
| `test_config_functions.py` | Tests configuration utility functions in `config/functions.py` |
| `test_result_file.py` | Tests result file parsing and handling |
| `test_wafermap_file.py` | Tests wafer map file parsing functionality |
| `test_config.py` | Tests TOML configuration file parsing and validation |

## Best Practices for Running Tests

### 1. Regular Execution
Run tests frequently during development:
```bash
# After making changes
python -m pytest tests/ -x
```
The `-x` flag stops on first failure for quick feedback.

### 2. Before Committing
Always run the full test suite before committing changes:
```bash
python -m pytest tests/ --tb=short
```

### 3. Continuous Integration
In CI environments, consider running with:
```bash
python -m pytest tests/ --verbose --tb=line --maxfail=5
```

### 4. Debugging Failed Tests
When a test fails:
1. Run that specific test with verbose output: `python -m pytest tests/test_name.py::test_function -v -s`
2. Examine the traceback carefully
3. Check if temporary files are being cleaned up properly
4. Verify mock objects are set up correctly

## Troubleshooting

### Common Issues

#### Missing Dependencies
If you see `ModuleNotFoundError`:
```bash
pip install -r requirements_dev.txt
```

#### Import Errors
If tests fail to import modules:
- Ensure you're running from the project root directory
- Check that `__init__.py` files exist in all package directories
- Verify PYTHONPATH includes the project root

#### Permission Errors
On Windows, if you encounter permission issues:
- Run Command Prompt or PowerShell as Administrator
- Or adjust directory permissions for the test output folders

#### Test Isolation Problems
If tests interfere with each other:
- Ensure each test properly cleans up temporary resources
- Verify that mock objects don't retain state between tests
- Check that global variables are reset appropriately

## Advanced Testing Techniques

### Parameterized Tests
Some tests use parameterization to test multiple inputs:
```python
# Example pattern used in test suites
@pytest.mark.parametrize("input,expected", [
    ("value1", "result1"),
    ("value2", "result2"),
])
def test_function(input, expected):
    assert function(input) == expected
```

### Mocking External Dependencies
Tests use `unittest.mock` to isolate the system under test:
```python
# Example from test_common_save_results.py
main = MagicMock()
main.ui.txtProcess.text.return_value = "TEST_PROCESS"
```

### Temporary Directories
File system operations use temporary directories to avoid side effects:
```python
with tempfile.TemporaryDirectory() as temp_dir:
    # Perform file operations in temp_dir
    # Automatic cleanup when exiting context
```

## Continuous Integration Integration

The test suite is designed to work with CI systems like:
- GitHub Actions
- GitLab CI
- Jenkins
- Azure Pipelines

Typical CI configuration would include:
1. Checkout code
2. Set up Python environment
3. Install dependencies: `pip install -r requirements_dev.txt`
4. Run tests: `python -m pytest tests/ --tb=short --maxfail=5`
5. Publish test results
6. Optionally: Generate and publish coverage reports

## Maintenance Guidelines

### Adding New Tests
When adding new functionality:
1. Create a new `test_*.py` file in the `tests/` directory
2. Follow existing naming conventions
3. Ensure tests are independent and deterministic
4. Use appropriate mocks and temporary directories
5. Test both positive and negative cases
6. Test edge cases and boundary conditions

### Maintaining Existing Tests
When modifying code:
1. Run the full test suite before making changes
2. If tests fail, determine if the failure is expected due to your changes
3. Update tests only if the behavior change is intentional
4. Never modify tests to make them pass without fixing the underlying issue
5. After fixing code, verify all related tests pass

## Conclusion

The Caracterizar project maintains a robust test suite that validates core functionality, with particular emphasis on the unified measurement results saving system. By following the procedures outlined in this guide, developers can ensure code quality, prevent regressions, and maintain confidence in the software's reliability.

Regular test execution, combined with proper test maintenance practices, forms a critical part of the project's quality assurance process.