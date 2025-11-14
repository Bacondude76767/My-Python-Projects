DO NOT SUSPECT THEESE TO WORK

theese may not work on your thing, if it dosnt please contact me
theese files are only python, nothing else, also make sure
you have PIP installed, and a working browser, some of the code i put on here
require websites, like my calc code, it requiers a html website for the curency
converter, 


For some of my code, you need to download a couple of batch files,
if you dont know how to please use this,




@echo off
REM -------------------------
REM All-in-One Setup & Run
REM -------------------------

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install required packages
echo Installing dependencies...
pip install pillow tkinterdnd2

REM Run the Python application
echo Starting app...
python your_script_name.py

pause

