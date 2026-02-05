@echo off
setlocal

set "SCRIPT_DIR=%~dp0"

python "%SCRIPT_DIR%inno\update_version.py"
if errorlevel 1 exit /b 1

set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"

if not exist "%ISCC%" (
  echo Inno Setup Compiler ISCC.exe nicht gefunden.
  echo Bitte Inno Setup installieren oder den Pfad in diesem Script anpassen.
  exit /b 1
)

set "ROOT_DIR=%SCRIPT_DIR%.."
for %%I in ("%ROOT_DIR%") do set "ROOT_DIR=%%~fI"
set "DIST_DIR=%ROOT_DIR%\\dist\\WingShape-Analyzer"
if not exist "%DIST_DIR%" (
  echo Dist-Ordner nicht gefunden: %DIST_DIR%
  echo Bitte zuerst PyInstaller ausfuehren. Siehe doku\\setup_guide.md
  exit /b 1
)

"%ISCC%" "%SCRIPT_DIR%inno\WingShape-Analyzer.iss"
