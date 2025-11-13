@echo off
chcp 65001 > nul
title Whitelist Application

echo ========================================
echo    Whitelist Resources Application
echo ========================================
echo.

if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt > nul 2>&1

echo Запуск приложения...
python run_service.py

pause