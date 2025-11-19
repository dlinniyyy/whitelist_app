import os
import sys
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import threading
import traceback
from waitress import serve

# Добавляем путь к текущей директории
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)


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

        # Логирование при инициализации
        self.log("Служба инициализирована")

    def log(self, message):
        """Простое логирование в файл"""
        try:
            log_path = os.path.join(os.path.dirname(__file__), "service_log.txt")
            with open(log_path, "a", encoding="utf-8") as f:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] {message}\n")
        except Exception as e:
            # Если не можем записать в файл, пробуем записать в системный лог
            try:
                servicemanager.LogInfoMsg(f"Ошибка логирования: {e}")
            except:
                pass

    def SvcStop(self):
        """Остановка службы"""
        self.log("Получена команда остановки службы")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        win32event.SetEvent(self.hWaitStop)
        self.log("Служба остановлена")

    def SvcDoRun(self):
        """Запуск службы"""
        self.log("Запуск службы SvcDoRun")
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))

        try:
            self.log("Установка статуса SERVICE_RUNNING")
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log("Статус установлен")

            self.is_running = True
            self.main()

        except Exception as e:
            self.log(f"ОШИБКА в SvcDoRun: {str(e)}")
            self.log(traceback.format_exc())
            servicemanager.LogErrorMsg(f"Ошибка запуска службы: {e}")

    def run_server(self):
        """Запуск сервера в отдельном потоке"""
        self.log("Запуск сервера в отдельном потоке")
        try:
            # Меняем рабочую директорию на директорию скрипта
            os.chdir(os.path.dirname(__file__))
            self.log(f"Рабочая директория: {os.getcwd()}")

            from app_production import app
            self.log("Импорт app_production выполнен успешно")

            # Создаем бэкап при запуске
            try:
                from app_production import create_backup
                self.log("Создание бэкапа при запуске...")
                if create_backup():
                    self.log("Бэкап создан успешно")
                else:
                    self.log("Ошибка создания бэкапа")
            except Exception as e:
                self.log(f"Ошибка при создании бэкапа: {e}")

            self.log("Запуск Waitress сервера...")
            serve(app, host='127.0.0.1', port=5001, threads=2, channel_timeout=300)
            self.log("Waitress сервер запущен")

        except Exception as e:
            self.log(f"ОШИБКА в run_server: {str(e)}")
            self.log(traceback.format_exc())

    def main(self):
        """Основной метод службы"""
        self.log("Вход в main() метод")
        try:
            # Быстро сообщаем, что служба запускается
            self.log("Запуск серверного потока")

            # Запускаем сервер в отдельном потоке
            self.server_thread = threading.Thread(target=self.run_server)
            self.server_thread.daemon = True
            self.server_thread.start()

            self.log("Серверный поток запущен")
            servicemanager.LogInfoMsg("Служба WhitelistService запущена успешно")
            self.log("Служба WhitelistService запущена успешно")

            # Короткий цикл ожидания
            counter = 0
            while self.is_running and counter < 300:  # 5 минут максимум
                time.sleep(1)
                counter += 1
                if counter % 30 == 0:  # Логируем каждые 30 секунд
                    self.log(f"Служба работает... ({counter} сек)")

            self.log("Выход из основного цикла")

        except Exception as e:
            self.log(f"ОШИБКА в main: {str(e)}")
            self.log(traceback.format_exc())
        finally:
            self.log("Завершение работы службы")


def usage():
    print("Использование:")
    print("  install_service_fixed.py install    - установить службу")
    print("  install_service_fixed.py start      - запустить службу")
    print("  install_service_fixed.py stop       - остановить службу")
    print("  install_service_fixed.py remove     - удалить службу")
    print("  install_service_fixed.py restart    - перезапустить службу")
    print("  install_service_fixed.py debug      - запуск в режиме отладки")


if __name__ == '__main__':
    # Создаем лог файл в текущей директории
    try:
        log_path = os.path.join(os.path.dirname(__file__), "service_log.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n{'=' * 50}\n")
            f.write(f"Запуск: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Аргументы: {sys.argv}\n")
            f.write(f"Текущая директория: {os.getcwd()}\n")
            f.write(f"Директория скрипта: {os.path.dirname(__file__)}\n")
    except Exception as e:
        print(f"Ошибка создания лога: {e}")

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
            try:
                # Меняем директорию на директорию скрипта
                os.chdir(os.path.dirname(__file__))
                from app_production import app
                from waitress import serve

                print(f"Запуск сервера в директории: {os.getcwd()}")
                serve(app, host='127.0.0.1', port=5001, threads=2)
            except Exception as e:
                print(f"Ошибка: {e}")
                traceback.print_exc()
                input("Нажмите Enter для выхода...")
        else:
            # Управление службой
            win32serviceutil.HandleCommandLine(WhitelistService)