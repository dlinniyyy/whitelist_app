@echo off
chcp 65001 > nul
title Управление бэкапами Whitelist

echo ========================================
echo    Управление бэкапами Whitelist
echo ========================================
echo.

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Запуск менеджера бэкапов...
python backup_manager.py

pause