@echo off
powershell -Command "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File \"%~dp0deps.ps1\"' -Verb RunAs -Wait"
pause
