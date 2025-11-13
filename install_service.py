import os
import sys
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import threading
from waitress import serve
from app_production import app, create_backup


class WhitelistService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WhitelistService"
    _svc_display_name_ = "Whitelist Resources Service"
    _svc_description_ = "Служба для управления полезными ресурсами ГБУ РО «ЦГБ им. Н.А. Семашко»"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = False
        self.server_thread = None
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """Остановка службы с созданием бэкапа"""
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False

        # Создаем бэкап перед остановкой
        servicemanager.LogInfoMsg("Создание бэкапа перед остановкой службы...")
        if create_backup():
            servicemanager.LogInfoMsg("Бэкап создан успешно")
        else:
            servicemanager.LogErrorMsg("Ошибка создания бэкапа")

        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """Запуск службы с созданием бэкапа"""
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))

        # Создаем бэкап при запуске
        servicemanager.LogInfoMsg("Создание бэкапа при запуске службы...")
        if create_backup():
            servicemanager.LogInfoMsg("Бэкап создан успешно")
        else:
            servicemanager.LogErrorMsg("Ошибка создания бэкапа")

        self.is_running = True
        self.main()

    def run_server(self):
        """Запуск сервера в отдельном потоке"""
        try:
            serve(app, host='0.0.0.0', port=5000, threads=4)
        except Exception as e:
            servicemanager.LogErrorMsg(f"Ошибка сервера: {e}")

    def main(self):
        """Основной метод службы"""
        try:
            # Запускаем сервер в отдельном потоке
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_thread.start()

            servicemanager.LogInfoMsg("Служба WhitelistService запущена успешно")

            # Ждем сигнала остановки
            while self.is_running:
                time.sleep(1)

        except Exception as e:
            servicemanager.LogErrorMsg(f"Ошибка в службе: {e}")
        finally:
            servicemanager.LogInfoMsg("Служба WhitelistService остановлена")


def usage():
    print("Использование:")
    print("  install_service.py install    - установить службу")
    print("  install_service.py start      - запустить службу")
    print("  install_service.py stop       - остановить службу")
    print("  install_service.py remove     - удалить службу")
    print("  install_service.py restart    - перезапустить службу")
    print("  install_service.py debug      - запуск в режиме отладки")
    print("  install_service.py backup     - создать бэкап вручную")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Режим службы
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WhitelistService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        # Режим командной строки
        if sys.argv[1] == 'debug':
            # Режим отладки
            print("Запуск в режиме отладки...")
            from waitress import serve
            from app_production import app, create_backup

            # Создаем бэкап при запуске
            print("Создание бэкапа...")
            if create_backup():
                print("Бэкап создан успешно")
            else:
                print("Ошибка создания бэкапа")

            serve(app, host='0.0.0.0', port=5000, threads=4)
        elif sys.argv[1] == 'backup':
            # Ручное создание бэкапа
            from app_production import create_backup

            print("Создание бэкапа вручную...")
            if create_backup():
                print("Бэкап создан успешно")
            else:
                print("Ошибка создания бэкапа")
        else:
            # Управление службой
            win32serviceutil.HandleCommandLine(WhitelistService)