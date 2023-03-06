from dotenv import dotenv_values
from generate_serial import new_serial
from mkg1000 import Printer
from read_relay import RelayNode
from serial_db import Database
from time import time, sleep

# = Configure app =============================================================

MIN_PANEL_FREQUENCY = 5

config = dotenv_values()

# ============================================================================


if __name__ == '__main__':

    db = Database(config["DB_SERVER"], config["DB_NAME"], config["DB_USERNAME"], config["DB_PASSWD"])
    printer = Printer(config["MKG1000_PRINTER_IP"], int(config["MKG1000_PRINTER_PORT"]))
    relay = RelayNode(config["RELAY_PORT"])

    has_serial = False
    is_triggered = False

    last_update = time()

    while True:

        this_time = time()

        # Printer needs serial number in before photoeye trigger order to respond in time.
        if not has_serial:

            # Send serial number to printer and acknowledge reciept of serial.
            serial_number = new_serial()
            if printer.send_serial(serial_number):
                has_serial = True

        # The photoeye triggering causes printer to write serial number.
        if (relay.read_state() == "Closed") and not is_triggered and ((this_time - last_update) > MIN_PANEL_FREQUENCY):

            # This means serial printer has written.
            is_triggered = True

        # If photoeye is triggered from panel passing under it.
        if is_triggered and has_serial:

            carrier_number = None  # TODO: Capture scanned carrier #

            # Send serial number that was written to database.
            db.add_panel(serial_number, carrier_number, config["LINE"], config["LOCATION"])
            # print(serial_number)
            is_triggered = False
            has_serial = False
            last_update = this_time
            sleep(1)
