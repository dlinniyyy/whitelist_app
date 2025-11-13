import os
import sys
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from waitress import serve
from app_production import app

class WhitelistService(win32serviceutil.ServiceFramework):
    _svc_name_ = "WhitelistService"
    _svc_display_name_ = "Whitelist Resources Service"
    _svc_description_ = "Служба для управления полезными ресурсами ГБУ РО «ЦГБ им. Н.А. Семашко»"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Запускаем приложение
        serve(app, host='0.0.0.0', port=5000, threads=4)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(WhitelistService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(WhitelistService)