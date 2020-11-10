@ECHO OFF

:: source the python environment
ECHO ## Activating Virtual Environment:
SET SOURCE=%CD%\.venv\Scripts\activate.bat
CALL %SOURCE%

:: run the application
ECHO ## Starting Application:
SET SCRIPTPATH=%CD%\src\main.py
CALL python %SCRIPTPATH%

