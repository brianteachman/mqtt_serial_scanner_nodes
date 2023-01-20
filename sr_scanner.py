#import asyncio
import socket
from time import sleep

SCANNER_HOST =  "198.168.1.54"
SCANNER_PORT = 9004            # socket server port number

# Scanner ASCII Commands ------------------------------------------------------

MESSAGE = b'LON[CR]',

# -----------------------------------------------------------------------------


"""
Class for Communication with an SR1000 Keyence Scanner
"""
class SRScanner:

    def __init__(self, logger=None):
        self.conn = None  # Socket Connection
        self.connected = False
        self.log = logger
        self.connect()

    def tx(self, message):
        self.conn.send(message)  # send message
        sleep(.1)

    def rx(self):
        data = self.conn.recv(1024).decode()  # receive response
        print('Received from scanner: ' + data)
        # self.log.info('Received from scanner: ' + data)
        return data

    # Initiate a connection to the SR1000
    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket Connection
        try:
            self.conn.connect((SCANNER_HOST, SCANNER_PORT))  # connect to the server
            sleep(.1)
            data = self.rx()  # TODO: waht does this response contain?
            self.connected = True
            print(f"Connected to {SCANNER_HOST}:{SCANNER_PORT}")
            # self.log.info(f"Connected to {SCANNER_HOST}:{SCANNER_PORT}")
        except socket.error as er:
            print(f"Connection Failed: {er}")
            # self.log.error(f"Connection to {SCANNER_HOST}:{SCANNER_PORT} Failed")
        
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


if __name__ == '__main__':

    s = SRScanner()

    print(s.req(MESSAGE))
