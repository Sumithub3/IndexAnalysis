@ECHO OFF
REM ANALYSIS IS STARTING.....

SET PYTHON="D:\IndexDataAnalysisAutomation\venv\scripts\python.exe"

%PYTHON% "D:\IndexDataAnalysisAutomation\DownloadNSEData.py" >> "D:\IndexDataAnalysisAutomation\run_scripts\scripts_output.log" 2>&1
REM ANALYSIS IS STARTED...
PAUSE