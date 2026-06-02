@echo off
title Zamil Full-Stack Runner
echo ======================================================================
echo                Zamil Full-Stack Project - One-Click Launcher
echo ======================================================================
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run_project.ps1"
echo.
echo ======================================================================
echo Press any key to exit.
pause > nul
