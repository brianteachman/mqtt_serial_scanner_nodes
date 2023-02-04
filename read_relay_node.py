import serial
import time


if __name__ == '__main__':
    print("Running Serial test.")

    # Open a serial connection
    s = serial.Serial("COM5", 115200)

    # Read serial data from uController relay
    while True:
        print(s.readline().strip())
        time.sleep(.1)
