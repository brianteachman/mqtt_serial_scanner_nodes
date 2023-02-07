from generate_serial import new_serial
from mkg1000 import Printer
from mssql_dal import Database
from dotenv import dotenv_values
from serial import Serial
from time import sleep

config = dotenv_values()


if __name__ == '__main__':

    printer = Printer(config["MKG1000_PRINTER_IP"], config["MKG1000_PRINTER_PORT"])
    usb = Serial("COM5", 115200)
    db = Database(config["DB_ADDRESS"])

    has_serial = False
    is_triggered = False

    while True:

        # Printer needs serial number in before photoeye trigger order to respond in time.
        if not has_serial:

            # Send serial number to printer and acknowledge reciept opf serial.
            serial_number = new_serial()
            if printer.send_serial(serial_number):
                has_serial = True
                # continue

        # The photoeye triggering causes printer to write serial number.
        is_triggered = usb.readline()
        # This means serial printer has written.

        # If photoeye is triggered from panel passing under it.
        if is_triggered and has_serial:

            # send serial number that was written to database
            db.update_panel(serial_number, "Serial Printer")
            is_triggered = False
            has_serial = False
            sleep(.1)
