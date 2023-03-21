from python_service import PythonService
from main import app
import logging

logging.basicConfig(filename='C:\\bin\\serial_controller\\data\\service.log', encoding='utf-8', level=logging.DEBUG)


class SerialPrinterService(PythonService):

    # Inherited class members
    _svc_name_ = "SerialPrinterService"
    _svc_display_name_ = "Serial Printer Service"
    _svc_description_ = "Update inkjet printer with serial number to print and record to database."
    _exe_name_ = "C:\Program Files\Python311\Lib\site-packages\win32\pythonservice.exe"
    

    # Override the method to set the running condition
    def start(self):
        self.isrunning = True

    # Override the method to invalidate the running condition 
    # When the service is requested to be stopped.
    def stop(self):
        self.isrunning = False

    # Override the method to perform the service function
    def main(self):

        while self.isrunning:
            try:
                app.run(self.isrunning)
            except Exception as err:
                logging.error(err)
                self.stop()


# Use this condition to determine the execution context.
if __name__ == '__main__':
    # Handle the command line when run as a script
    SerialPrinterService.parse_command_line()
