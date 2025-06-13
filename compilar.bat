@echo off
Rem Compiling main.ui
pyside6-uic main.ui> ui_main.py
Rem copy to folder modules
copy ui_main.py modules\ui_main.py