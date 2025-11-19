@echo off
chcp 65001
title Переустановка Whitelist Service

echo ========================================
echo    ПЕРЕУСТАНОВКА СЛУЖБЫ
echo ========================================
echo.

echo Остановка службы...
python install_service_fixed.py stop
timeout /t 3 /nobreak > nul

echo Удаление старой службы...
python install_service_fixed.py remove
timeout /t 2 /nobreak > nul

echo Очистка логов...
del service_log.txt 2>nul
del app_log.txt 2>nul

echo Установка новой службы...
python install_service_fixed.py install
timeout /t 2 /nobreak > nul

echo Запуск службы...
python install_service_fixed.py start
timeout /t 5 /nobreak > nul

echo Диагностика...
python diagnose_service.py

echo.
echo Готово! Проверьте службу.
pause