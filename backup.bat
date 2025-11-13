@echo off
chcp 65001 > nul
title Создание бэкапа Whitelist

echo ========================================
echo    Создание бэкапа Whitelist
echo ========================================
echo.

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Создание бэкапа...
python install_service.py backup

echo.
pause