@echo off
chcp 65001 > nul
title Удаление Whitelist Service

echo ========================================
echo    Удаление Whitelist Service
echo ========================================
echo.

echo Остановка службы...
python force_stop_service.py

echo.
echo Удаление службы...
python install_service.py remove

echo.
echo Служба удалена!
echo.
pause