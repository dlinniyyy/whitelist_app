@echo off
chcp 65001 > nul
title Перезапуск Whitelist Service

echo ========================================
echo    Перезапуск Whitelist Service
echo ========================================
echo.

echo Остановка службы...
python install_service.py stop
timeout /t 3 /nobreak > nul

echo Запуск службы...
python install_service.py start

echo.
echo Служба перезапущена!
echo Проверьте: http://localhost:5001
echo.
pause