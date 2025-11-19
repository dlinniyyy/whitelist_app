import os
import sys
import time
import subprocess
import win32service
import win32serviceutil


def get_script_directory():
    """Получить директорию скрипта"""
    return os.path.dirname(os.path.abspath(__file__))


def check_service_status(service_name):
    """Проверка статуса службы"""
    try:
        status = win32serviceutil.QueryServiceStatus(service_name)
        state = status[1]

        states = {
            win32service.SERVICE_STOPPED: "Остановлена",
            win32service.SERVICE_START_PENDING: "Запускается",
            win32service.SERVICE_STOP_PENDING: "Останавливается",
            win32service.SERVICE_RUNNING: "Выполняется",
            win32service.SERVICE_CONTINUE_PENDING: "Продолжается",
            win32service.SERVICE_PAUSE_PENDING: "Приостанавливается",
            win32service.SERVICE_PAUSED: "Приостановлена"
        }

        return states.get(state, f"Неизвестно ({state})")
    except Exception as e:
        return f"Ошибка: {e}"


def diagnose_service():
    """Диагностика службы"""
    service_name = "WhitelistService"
    script_dir = get_script_directory()

    print("=" * 50)
    print("ДИАГНОСТИКА СЛУЖБЫ WHITELISTSERVICE")
    print("=" * 50)
    print(f"Директория приложения: {script_dir}")
    print()

    # 1. Проверка статуса службы
    print(f"1. Статус службы: {check_service_status(service_name)}")

    # 2. Проверка файлов
    print("\n2. Проверка файлов:")
    essential_files = [
        "app_production.py",
        "templates/index.html",
        "templates/admin.html",
        "data/resources.json",
        "install_service_fixed.py"
    ]

    for file in essential_files:
        file_path = os.path.join(script_dir, file)
        exists = os.path.exists(file_path)
        print(f"   {file}: {'✅' if exists else '❌'}")

    # 3. Проверка порта
    print("\n3. Проверка порта 5001:")
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5001))
        print(f"   Порт 5001: {'🔴 Занят' if result == 0 else '🟢 Свободен'}")
        sock.close()
    except Exception as e:
        print(f"   Ошибка проверки порта: {e}")

    # 4. Проверка логов
    print("\n4. Логи службы:")
    log_files = [
        "service_log.txt",
        "logs/whitelist.log",
        "app_log.txt"
    ]

    for log_file in log_files:
        log_path = os.path.join(script_dir, log_file)
        if os.path.exists(log_path):
            size = os.path.getsize(log_path)
            print(f"   {log_file}: {size} байт")
        else:
            print(f"   {log_file}: ❌ Не найден")

    # 5. Рекомендации
    print("\n5. Рекомендации:")
    status = check_service_status(service_name)

    if "Ошибка" in status:
        print("   🔧 Установите службу заново")
    elif "Останавливается" in status or "Запускается" in status:
        print("   ⏳ Подождите завершения операции")
    elif "Выполняется" in status:
        print("   ✅ Служба работает, проверьте http://localhost:5001")
    else:
        print("   🚀 Запустите службу")


if __name__ == '__main__':
    diagnose_service()
    input("\nНажмите Enter для выхода...")