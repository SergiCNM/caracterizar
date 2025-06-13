# Caracterizar

## Introduction

**Caracterizar** is a powerful GUI-based software designed for electrical characterization of semiconductor devices. The software provides seamless integration of laboratory instruments such as **semiconductor parameter analyzers, impedance analyzers, and probe stations**, allowing users to execute both individual device tests and complete wafer-level measurements.

The GUI is based on the [Modern GUI PyDracula framework by Wanderson-Magalhaes](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6), offering a clean, modern, and user-friendly interface.

With **Caracterizar**, you can:

* Perform single-device measurements.
* Carry out full-wafer cartography measurements.
* Visualize and interact with wafer maps.
* Control prober stations and a variety of electrical measurement instruments.
* Automate measurement routines using configurable test files.

---

## Installation

### Prerequisites

* Python 3.9 or newer

### Windows

```bash
git clone https://github.com/yourusername/Caracterizar.git
cd Caracterizar
pip install -r requirements.txt
python main.py
```

### Linux / Unix

```bash
git clone https://github.com/yourusername/Caracterizar.git
cd Caracterizar
pip install -r requirements.txt
python3 main.py
```

### MacOS

```bash
git clone https://github.com/yourusername/Caracterizar.git
cd Caracterizar
pip install -r requirements.txt
python3 main.py
```

---

## Configuration Files

### `config.toml`

The `config.toml` file defines global settings for the application. It contains sections for:

* **Program Metadata**
* **Default Parameters**
* **Directory Structure**
* **File Names**
* **Database Connection**
* **Measurement Methods**

#### Example:

```toml
title = "Caracterizar"
version = "2.1.0"
author = "Sergi Sànchez"

[defaults]
debugmode = true
darkmode = false
txtprocess = "11234-12"
txtlot = "11234"
txtwafer = "12"

[dirs]
base = "config"
instruments = "instruments"
tests = "tests"
probers = "probers"
wafermaps = "wafermaps"
results = "results"
reports = "reports"

[mecao]
host = "opter6"
port = "5432"
user = "joaquin"
database = "mecao"

[labs]
mysqlhost = "localhost"
mysqluser = "root"
mysqlpassword = "Mysql123"
mysqldatabase = "labs_new"
```

### Key Sections:

* `defaults`: Predefined default values for process names, wafers, and measurement conditions.
* `dirs`: Directory paths for instruments, test scripts, probers, wafer maps, measurement results, and reports.
* `mecao` / `labs`: Database connection configurations for storing or retrieving measurement data.

---

### `devices.py`

This file specifies the list of supported instruments and probers with their connection settings.

#### Instrument Configuration Example:

```python
instruments["HP_4192A"] = {
    "address": 'GPIB0::23::INSTR',
    "read_termination": '\r\n',
    "write_termination": '\r\n',
    "timeout": '10000'
}
```

#### Supported Instruments:

* HP 4192A (Impedance Analyzer)
* HP 4155B (Parameter Analyzer)
* Keysight B1500 (LAN and GPIB support)
* Keithley 4200-SCS
* Keithley 2470
* LeCroy Oscilloscopes
* Keysight E4990A
* Deep Detection LINDA custom FPGA

#### Prober Configuration Example:

```python
probers["CNM_TEST"] = {
    "address": 'GPIB0::00::INSTR',
    "read_termination": '\n',
    "write_termination": '\n',
    "timeout": 10,
    "soft_contact": False
}
```

#### Supported Probers:

* CNM Test Prober
* MPI TS2000SE
* KARLSUSS PA200

Each prober can be configured to enable **progressive contact** with parameters like number of steps, max retries, and measurement strategies.

---

## Features

* ✅ Modern PySide6-based GUI
* ✅ Instrument and prober integration
* ✅ Wafer map visualization and cartography measurements
* ✅ Single-device and full-wafer automated tests
* ✅ Modular test configuration via Python scripts
* ✅ Results export and report generation
* ✅ Database connection support
* ✅ Multi-platform compatibility (Windows, Linux, MacOS)

---

## License

This project is released under the MIT License.

---

## Acknowledgments

* GUI framework: [Modern GUI PyDracula by Wanderson-Magalhaes](https://github.com/Wanderson-Magalhaes/Modern_GUI_PyDracula_PySide6_or_PyQt6)
* Program design and development: Sergi Sànchez
