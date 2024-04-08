from python_service import PythonService
from main import app
from logit import get_logger

logger = get_logger(__name__)


class SerialPrinterService(PythonService):

    # Inherited class members
    _svc_name_ = "SerialPrinterService"
    _svc_display_name_ = "Serial Printer Service"
    _svc_description_ = "Update inkjet printer with serial number to print and record to database."
    _exe_name_ = "C:\\Program Files\\Python311\\Lib\\site-packages\\win32\\pythonservice.exe"
    
    def start(self):
        ''' Override the method to set the running condition '''
        self.isrunning = True

    #
    def stop(self):
        '''
         Override the method to invalidate the running condition. 
         When the service is requested to be stopped.
         '''
        self.isrunning = False
        app.exit()

    # Override the method to perform the service function
    def main(self):
        ''' Main Application Windows Service Container '''
        while self.isrunning:
            try:
                app.step()
            except Exception as err:
                logger.error("Step Error: " + str(err))
                self.stop()

# Use this condition to determine the execution context.
if __name__ == '__main__':
    # Handle the command line when run as a script
    SerialPrinterService.parse_command_line()
