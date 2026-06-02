@echo off
title Zamil APK Compiler
echo ======================================================================
echo                Zamil APK Compiler - One-Click Builder
echo ======================================================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0build_apk.ps1"
echo.
echo ======================================================================
echo Press any key to exit.
pause > nul
