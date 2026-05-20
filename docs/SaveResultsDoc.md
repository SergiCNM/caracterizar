# Save Results Documentation

This document describes the unified approach for saving measurement results in the Caracterizar software, ensuring consistent file format and folder structure across all instrument tests.

## Overview

All instrument tests now use a common function `save_results_to_file()` from `config/default/tests/common.py` to save measurement data. This ensures:

- Consistent columnated text file format
- Standardized folder structure: `results/<username>/<process>/<lot>_W<wafer>/`
- Unified file naming convention
- Centralized formatting logic

## Common Functions

### `build_results_folder()`

Builds the standard results folder path.

**Parameters:**
- `username` (str): Username from test configuration
- `process` (str): Process name from `main.ui.txtProcess.text()`
- `lot` (str): Lot name from `main.ui.txtLot.text()`
- `wafer` (str/int): Wafer number from `main.ui.txtWafer.text()`

**Returns:**
- `str`: Folder path in format `cwd/results/username/process/lot_Wwafer/`

**Example:**
```python
folder = build_results_folder(
    username="testuser",
    process="IV_Test",
    lot="LOT123",
    wafer=5
)
# Returns: "C:/path/to/results/testuser/IV_Test/LOT123_W05/"
```

### `save_results_to_file()`

Saves measurement results to a columnated text file.

**Parameters:**
- `results_data` (list): Data to save (list of lists or single list)
- `variables_list` (list): Variable names for CSV header
- `test_parameters` (dict): Contains:
  - `separator`: "space", "tab", or "comma" (default)
  - `prefix`: Optional filename prefix
  - `suffix`: Optional filename suffix
  - `variables`: Comma-separated string of variable names (e.g., "V,I,C")
- `die` (int): Die number
- `module` (int): Module number
- `folder_func` (callable): Function returning folder path string

**Returns:**
- `str`: Full filepath of saved file

**File Naming Logic:**
- If prefix and suffix: `{prefix}_{die}_{module}_{suffix}.txt`
- If prefix only: `{prefix}_{die}_{module}.txt`
- If suffix only: `{die}_{module}_{suffix}.txt`
- If neither: `{die}_{module}.txt`

## Usage in Tests

### Step 1: Import Functions
```python
from config.default.tests.common import save_results_to_file, build_results_folder
```

### Step 2: Add Required Global Variables
Ensure these are declared in your test's global section:
```python
global results_dir, username  # If not already present
```

### Step 3: Prepare Data and Parameters
```python
# Prepare measurement data
results_data = list(zip(voltage, current, capacitance))  # Example
variables_list = ["V", "I", "C"]

# Get output parameters from TOML (should include [output] section)
output_params = test_parameters.get("output", {
    "separator": "comma", 
    "prefix": "TEST", 
    "suffix": "",
    "variables": "V,I,C"  # Comma-separated string, NOT array
})
```

### Step 4: Call save_results_to_file
```python
save_results_to_file(
    results_data=results_data,
    variables_list=variables_list,
    test_parameters=output_params,
    die=dieActual,
    module=moduleActual,
    folder_func=lambda: build_results_folder(
        username=username,
        process=main.ui.txtProcess.text(),
        lot=main.ui.txtLot.text(),
        wafer=main.ui.txtWafer.text()
    )
)
```

## TOML Configuration Requirements

Each test's TOML file must include an `[output]` section:

```toml
[output]
separator = "comma"
prefix = "TEST_NAME"   # Optional
suffix = ""            # Optional
variables = "V,I,C"    # Comma-separated string (NOT array)
```

## Updated Tests

The following tests have been updated to use the common save function:

### HP_4192A
- CV_test.py
- CW_test.py
- CV_IV_external_test.py
- CV_IV_ring_external_test.py

### Keysight_E4990A
- CV_test.py
- CW_test.py
- CV_IV_external_test.py
- CV_IV_ring_external_test.py
- CV_nanusens_test.py
- CV_RF_nanusens_test.py

### Keithley_4200
- CV_test.py
- CW_test.py

### Keithley_2470
- IV_test.py
- IV4_test.py
- IV_ring_test.py

### Keithley_2410
- IV_ring_test.py

### Keysight_B1500LAN
- Test_test.py

## Benefits

1. **Consistency**: All tests save files in the same format and location
2. **Maintainability**: Changes to save logic only needed in one place
3. **Reduced Duplication**: Eliminates repetitive file-saving code
4. **Standardized Naming**: Predictable file names based on die/module
5. **Flexible Format**: Supports comma, space, or tab separators via TOML

## Adding New Tests

When creating new instrument tests:

1. Import the common functions:
   ```python
   from config.default.tests.common import save_results_to_file, build_results_folder
   ```

2. Add required globals:
   ```python
   global results_dir, username  # Add to existing globals
   ```

3. Prepare your data as lists suitable for zipping
4. Define variables_list matching your data columns
5. Ensure your TOML has an [output] section with variables as comma-separated string
6. Call save_results_to_file with the lambda folder_func as shown above

## Example Complete Implementation

```python
# In your test file
from config.default.tests.common import save_results_to_file, build_results_folder

# ... globals including results_dir, username ...

def save_measurement_data(main, voltage, current, capacitance):
    """Example function showing complete usage"""
    global dieActual, moduleActual
    
    # Prepare data
    results_data = list(zip(voltage, current, capacitance))
    variables_list = ["V", "I", "C"]
    
    # Get parameters (assuming they're loaded elsewhere)
    test_parameters = {"output": {"separator": "comma", "prefix": "MYTEST", "suffix": "", "variables": "V,I,C"}}
    
    # Save using common function
    save_results_to_file(
        results_data=results_data,
        variables_list=variables_list,
        test_parameters=test_parameters,
        die=dieActual,
        module=moduleActual,
        folder_func=lambda: build_results_folder(
            username=username,
            process=main.ui.txtProcess.text(),
            lot=main.ui.txtLot.text(),
            wafer=main.ui.txtWafer.text()
        )
    )
```