@echo off
REM Build HAC Autoclicker

cd /d %~dp0

set SCRIPT=src\main.py
set EXE_NAME=HAC_Autoclicker.exe
set ICON=src\assets\icon.ico

python -m PyInstaller --onefile --noconsole --icon="%ICON%" --add-data "src\assets\icon.ico;assets" "%SCRIPT%"

rmdir /s /q build
del main.spec

echo %EXE_NAME% successfully generated!
pause
