@echo off
chcp 65001 > nul
title Управление Whitelist Service

:menu
cls
echo ========================================
echo    Управление Whitelist Service
echo ========================================
echo.
echo 1 - Установить службу
echo 2 - Запустить службу
echo 3 - Остановить службу
echo 4 - Перезапустить службу
echo 5 - Удалить службу
echo 6 - Принудительная остановка
echo 7 - Запуск в режиме отладки
echo 8 - Выход
echo.
set /p choice="Выберите действие: "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto restart
if "%choice%"=="5" goto remove
if "%choice%"=="6" goto force_stop
if "%choice%"=="7" goto debug
if "%choice%"=="8" goto exit

echo Неверный выбор!
timeout /t 2 /nobreak > nul
goto menu

:install
python install_service.py install
pause
goto menu

:start
python install_service.py start
pause
goto menu

:stop
python install_service.py stop
pause
goto menu

:restart
call restart_service.bat
goto menu

:remove
call uninstall_service.bat
goto menu

:force_stop
python force_stop_service.py
pause
goto menu

:debug
python install_service.py debug
pause
goto menu

:exit
echo Выход...