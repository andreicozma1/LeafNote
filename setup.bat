@ECHO OFF


echo ## Checking Python Version (MUST BE VERSION 3.8 OR UNDER):
set COMMAND=where python3 2> nul
for /f %%i in ('%COMMAND%') do @set LOCATION=%%i
if %LOCATION%=="" (
    ECHO ## ERROR: Python3 is not installed on your system!
    CALL :SHOWINSTALL
)
CALL python3 -V


echo ## Checking Pip3 Version:
set COMMAND=where pip3 2> nul
for /f %%i in ('%COMMAND%') do @set LOCATION=%%i
if %LOCATION%=="" (
    ECHO ## ERROR: Pip3 is not installed on your system!
    CALL :SHOWINSTALL
)
CALL pip3 -V

:: install virtual env if not already installed
CALL pip3 install virtualenv

:: create the virtual environment
ECHO ## Creating Virtual Environment:
SET VENV=%CD%\.venv
CALL python3 -m virtualenv %VENV%

:: source the python environment
ECHO ## Activating Virtual Environment:
SET SOURCE=%CD%\.venv\Scripts\activate.bat
CALL %SOURCE%

:: install requirements
ECHO ## Installing Project Dependencies:
SET REQS=%CD%\requirements.txt
CALL pip3 install -r %REQS%

ECHO ## All done!
PAUSE
EXIT

:SHOWINSTALL
ECHO # To proceed, please install Python3 and Pip3.
ECHO # Linux: sudo apt-get install python3 python3-pip
ECHO # macOS: brew install python3 python3-pip
ECHO # Windows: https://www.python.org/downloads
PAUSE
EXIT