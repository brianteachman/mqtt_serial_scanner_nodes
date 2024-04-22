from dotenv import dotenv_values
from generate_serial import new_serial
from mkg1000 import Printer
from read_relay import RelayNode
from serial_db import Database
from time import time, sleep
from logit import get_logger
import sys, os

os.chdir("C:\\bin\\serial_controller")

MIN_PANEL_FREQUENCY = 20


class MainApp():

    def __init__(self):
        ''' Class constructor'''
        self.log = get_logger(__name__, debug=False)

        # Setup domain objects
        self.env = dotenv_values()
        self.machine_name = self.env["MACHINE_NAME"]
        self.db = Database(self.env["DB_SERVER"], self.env["DB_NAME"], self.env["DB_USERNAME"], self.env["DB_PASSWD"])
        self.local_db = Database(self.env["LOCAL_DB_SERVER"], self.env["DB_NAME"], self.env["DB_USERNAME"], self.env["DB_PASSWD"])
        self.printer = Printer(self.env["MKG1000_PRINTER_IP"], int(self.env["MKG1000_PRINTER_PORT"]))
        self.relay = RelayNode(self.env["RELAY_PORT"])
        self.log.info("Loaded dependencies")

        # Setup state variables
        self.serial_number = None
        self.has_serial = False
        self.is_triggered = False
        self.first_run = True
        self.last_update = time()
        self.log.info("Serial Printer Service Initialized")

    def step(self):
        ''' The business logic '''

        this_time = time()
        self.log.info("Loaded step: " + str(this_time))

        # Printer needs serial number in before photoeye trigger order to respond in time.
        if not self.has_serial:
            self.log.info("Generate serial number")
            # Send serial number to printer and acknowledge reciept of serial.
            self.serial_number = new_serial(self.env)
            self.log.info("Sending to printer")
            if self.printer.send_serial(self.serial_number):
                self.has_serial = True
            self.log.info("Serial #" + self.serial_number + " loaded to printer")

        # The photoeye triggering causes printer to write serial number.
        if (self.relay.read_state() == "Closed") and not self.is_triggered and (((this_time - self.last_update) > MIN_PANEL_FREQUENCY) or self.first_run):

            if self.first_run:
                self.first_run = False
                
            # This means serial printer has written.
            self.is_triggered = True
            self.log.info("Panel present")

        # If photoeye is triggered from panel passing under it.
        if self.is_triggered and self.has_serial:

            carrier_number = None  # TODO: Capture scanned carrier #

            # Send serial number that was written to database.
            try:
                self.db.add_panel(self.machine_name, self.serial_number, carrier_number)
            except:
                self.local_db.add_panel(self.machine_name, self.serial_number, carrier_number)
            self.is_triggered = False
            self.has_serial = False
            self.serial_number = None
            self.last_update = this_time
            sleep(1)
            self.log.info("Updated database")


    def run(self, is_running=True):
        ''' Run the business logic in a loop '''

        while is_running:
            self.step()

    def exit(self):
        ''' Close COM port '''
        self.relay.close()


app = MainApp()

if __name__ == '__main__':
    app.run()
