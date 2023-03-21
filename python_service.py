# Reference:
# Mastromatteo, D. (2018): https://thepythoncorner.com/posts/2018-08-01-how-to-create-a-windows-service-in-python/
# Robinson, S. & Hammond, M. (2000). Python Programming on Win32. Sebastopol, CA: O'Reilly Media.
import win32event
import win32service
import win32serviceutil
from abc import ABC, abstractmethod

class PythonService(win32serviceutil.ServiceFramework, ABC):
    @classmethod
    def parse_command_line(cls):
        ''' Parse the command line '''
        win32serviceutil.HandleCommandLine(cls)

    # Override the method in the subclass to do something just before the service is stopped.
    @abstractmethod
    def stop(self):
        pass

    # Override the method in the subclass to do something at the service initialization.
    @abstractmethod
    def start(self):
        pass

    # Override the method in the subclass to perform actual service task.
    @abstractmethod
    def main(self):
        pass

    def __init__(self, args):
        ''' Class constructor'''
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Create an event which we will use to wait on.
        # The "service stop" request will set this event.
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        '''Called when the service is asked to stop'''
        # We may need to do something just before the service is stopped.
        self.stop()
        # Before we do anything, tell the SCM we are starting the stop process.
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # And set my event.
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''Called when the service is asked to start. The method handles the service functionality.'''
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        # We may do something at the service initialization.
        self.start()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Starts a worker loop waiting either for work to do or a notification to stop, pause, etc.
        self.main()
