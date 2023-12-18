@echo off

REM Set the path to your Miniconda Scripts directory
SET CONDA_SCRIPTS_PATH=C:\Users\%USERNAME%\mambaforge\Scripts

REM Activate your specific Conda environment and run the Python script
CALL %CONDA_SCRIPTS_PATH%\conda.exe run --no-capture-output -n base python src\main.py

echo Done.
pause