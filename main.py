from dotenv import dotenv_values
from generate_serial import new_serial
from mkg1000 import Printer
from read_relay import RelayNode
from serial_db import Database
from time import time, sleep
import os

os.chdir("C:\\bin\\serial_controller")

MIN_PANEL_FREQUENCY = 20


class MainApp():

    def __init__(self):
        ''' Class constructor'''

        # Setup domain objects
        config = dotenv_values()
        self.machine_name = config["MACHINE_NAME"]
        self.db = Database(config["DB_SERVER"], config["DB_NAME"], config["DB_USERNAME"], config["DB_PASSWD"])
        self.printer = Printer(config["MKG1000_PRINTER_IP"], int(config["MKG1000_PRINTER_PORT"]))
        self.relay = RelayNode(config["RELAY_PORT"])

        # Setup state variables
        self.has_serial = False
        self.is_triggered = False
        self.first_run = True
        self.last_update = time()
    
    def run(self, is_running=True):
        ''' Run the business logic '''

        while is_running:

            this_time = time()

            # Printer needs serial number in before photoeye trigger order to respond in time.
            if not self.has_serial:

                # Send serial number to printer and acknowledge reciept of serial.
                serial_number = new_serial()
                if self.printer.send_serial(serial_number):
                    self.has_serial = True

            # The photoeye triggering causes printer to write serial number.
            if (self.relay.read_state() == "Closed") and not self.is_triggered and (((this_time - self.last_update) > MIN_PANEL_FREQUENCY) or self.first_run):

                if self.first_run:
                    self.first_run = False
                    
                # This means serial printer has written.
                self.is_triggered = True

            # If photoeye is triggered from panel passing under it.
            if self.is_triggered and self.has_serial:

                carrier_number = None  # TODO: Capture scanned carrier #

                # Send serial number that was written to database.
                self.db.add_panel(self.machine_name, serial_number, carrier_number)
                # print(serial_number)
                self.is_triggered = False
                self.has_serial = False
                self.last_update = this_time
                sleep(1)


app = MainApp()

if __name__ == '__main__':
    app.run()
