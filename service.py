from win32serviceutil import ServiceFramework, HandleCommandLine
import win32service
import win32event
import servicemanager
import socket

from main_service import main_loop


class SerialControllerService (ServiceFramework):
    _svc_name_ = "SerialControllerService"
    _svc_display_name_ = "Serial Controller Service"

    def __init__(self,args):
        ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_,''))
        self.main()

    def main(self):
        main_loop()

if __name__ == '__main__':
    HandleCommandLine(SerialControllerService)