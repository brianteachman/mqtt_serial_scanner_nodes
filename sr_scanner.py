#import asyncio
import socket
from time import sleep

SCANNER_HOST =  "192.168.1.54"
SCANNER_PORT = 9004            # socket server port number


"""
Class for Communication with an SR1000 Keyence Scanner
"""
class SRScanner:

    def __init__(self, logger=None):
        self.conn = None  # Socket Connection
        self.connected = False
        self.log = logger
        self.connect()

    # Initiate a connection to the SR1000
    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket Connection
        self.conn.settimeout(10)
        try:
            self.conn.connect((SCANNER_HOST, SCANNER_PORT))  # connect to the server
            sleep(.1)
            # print(self.rx())
            self.connected = True
            print(f"Connected to {SCANNER_HOST}:{SCANNER_PORT}")
        except socket.error as er:
            print(f"Connection Failed: {er}")

    def tx(self, message):
        self.conn.sendall(message)  # send message

    def rx(self):
        data = self.conn.recv(1024).decode()  # receive response
        # print('Received from scanner: ' + data)
        return data
        
    # Send/Receive a Message
    def req(self, message):
        self.tx(message)  # send TCP message
        sleep(.1)
        data = self.rx()  # recieve TCP message
        return data
        # self.conn.close()  # close the connection

    # Request Status
    def getStatus(self):
        # return self.req(REQUEST_STATUS)
        pass

    # Send/Receive a Message
    def getSerial(self):
        # return str(self.req(REQUEST_FIELD_01)).replace('DATA,0,11,','')
        pass


# Scanner ASCII Commands ------------------------------------------------------

# Read Serial Number
TRIGGER_INPUT_ON = b'LON\r'
TRIGGER_INPUT_OFF = b'LOFF\r'

REQUEST_SCANNER_VERSION = b'KEYENCE\r'

REQUEST_TEST = b'TEST1\r'

# Set the timing mode to "One-shot trigger" (one-shot signal trigger)
SET_ONESHOT_TRIGGER = b'WP,101,1\r'
# Check if one shot trigger is set
IS_ONESHOT_TRIGGER = b'RP,101\r'

SET_TIME_APPENDING = b'WP,300,1\r'
IS_TIME_APPENDING = b'RP,300,1\r'

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    s = SRScanner()

    try:

        while True:
            # Fetch serial number
            print(s.req(TRIGGER_INPUT_ON))
            sleep(1)

    except KeyboardInterrupt:
        print("Done")
