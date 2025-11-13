@echo off
chcp 65001 > nul

echo Установка службы WhitelistService...

if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt
pip install pywin32

echo Установка службы...
python install_service.py install

echo Запуск службы...
python install_service.py start

echo.
echo Служба установлена и запущена!
echo Проверьте: http://localhost:5000
echo.
pause