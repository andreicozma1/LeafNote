@ECHO OFF

:: source the python environment
ECHO ## Activating Virtual Environment:
SET SOURCE=%CD%\.venv\Scripts\activate.bat
CALL %SOURCE%

:: move into the src directory and run the unit tests
ECHO ## Starting Tests
CD src/
CALL python -m unittest