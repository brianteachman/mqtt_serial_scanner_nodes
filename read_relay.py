import serial
import time


class RelayNode():

    def __init__(self) -> None:
        # Open a serial connection
        self.usb = serial.Serial("COM7", 115200)

    def read_state(self) -> str:
        line = self.usb.readline()
        self.usb.reset_input_buffer()
        return line.decode().replace("\r\n","")

    def close(self):
        self.usb.close()


if __name__ == '__main__':
    print("Running Serial test.")

    relay = RelayNode()

    try:
        # Read serial data from uController relay
        while True:

            print(relay.read_state())
        
            time.sleep(.1)
    except KeyboardInterrupt:
        relay.close()
