import socket
import asyncio
from time import sleep
from dotenv import dotenv_values


TERMINATOR = b'\r'

# Error Codes -----------------------------------------------------------------

"""
Error Response:

    ER,a,b

Where, a is a 2-byte command name that returned the error
      b is one of the 2-byte codes below representing the error
"""

ERROR_UNRECOGNIZABLE_COMMAND = 0
ERROR_BUSY = 1
ERROR_STATUS = 2
ERROR_PRIORITY = 3
ERROR_DATA_LENGTH = 20
ERROR_DATA_RANGE = 22
ERROR_MEMORY_OVER = 31
ERROR_TIMEOUT = 40
ERROR_INVALID_CHECKSUM = 90

# Error Commands --------------------------------------------------------------

# Request System's Status
REQUEST_SYSTEM_STATUS = b'SB\r'
"""
System Status Response: 

    SB,a

Where a is the current state change ID (see: SB-system-status-codes.PNG)
"""

# Request System's Error Status
REQUEST_SYSTEM_ERROR_STATUS = b'EV\r'
"""
Response: 

    EV,a

Where a is the number of the error or caution that is occurring (see: EV-{...}-level-error-codes.PNG)
"""

# Resets System's Error Status
RESET_SYSTEM_ERROR_STATUS = b'EZ\r'
# Responds with EZ after clearing errors


# SET_PRINT_STRING = f'FS,{a},{b},{c},{d}\r'
UPDATE_SERIAL_COMMAND = b'BE,4,1,'
# SET_PRINT_ASCII_MESSAGE = b'BE,4,1,1111111111W\r'
# REQUEST_CURRENT_BARCODE = b'BF,1,1\r'
REQUEST_CURRENT_BARCODE = b'BF,4,1\r'

# -----------------------------------------------------------------------------
REQUEST_TIMEOUT = 5

class Printer:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = socket.socket()
        self.conn.settimeout(REQUEST_TIMEOUT)
        self.connected = False
        self.connect()

    # Initiate a connection to Printer
    def connect(self):
        try:
            self.conn.connect((self.host, self.port))  # connect to the server
            self.connected = True
            print(f"Connected to {self.host}:{self.port}")
        except socket.error as exc:
            print(f"Connection to {self.host}:{self.port} Failed.")
            print(f"Recieved message: {exc}")

    def close(self):
        self.conn.close()
        self.connected = False


    # def request(self, message):
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.connect((self.host, self.port))
    #         s.sendall(message)
    #         sleep(.1)
    #         data = self.response(s)
    #     print('Received', repr(data))
    #     print('Completed')

    # def response(self, s):
    #     try:
    #         data = s.recv(1024).decode()  # receive response
    #         # print('Received from printer: ' + data)
    #     except TimeoutError:
    #         print(f"Connection to {self.host}:{self.port} timed out.")
    #         data = None
    #     return data

    def getResponse(self):
        try:
            # data = self.conn.recv(1024).decode()  # receive response
            data = self.conn.recv(1024)  # receive response
            # print('Received from printer: ' + data)
        except TimeoutError:
            print(f"Connection to {self.host}:{self.port} timed out.")
            data = None
        return data

    # Send/Receive a Message
    def req(self, message):
        # if not self.connected:
            # self.connect()

        self.conn.send(message)  # send message
        sleep(.1)
        data = self.getResponse()
        # self.close()  # close the connection
        return data

    def send_serial(self, serial_number):
        message = f'BE,4,1,{serial_number}\r'.encode()
        # if self.req(message).decode() == 'BE\r':
        if self.req(message) == b'BE\r':
            return True
        return False


if __name__ == "__main__":
    print("Running mkg1000 test.")

    c = dotenv_values()
    p = Printer(c["MKG1000_PRINTER_IP"], int(c["MKG1000_PRINTER_PORT"]))

    print(p.send_serial('2302130004W'))
    # print(p.req(REQUEST_CURRENT_BARCODE))

    # print(p.req(b'CN,4,1\r'))

    # print(p.req(REQUEST_SYSTEM_STATUS))
    # p.conn.sendall(b'FL\r')

    # Check for system errors
    # print(p.req(REQUEST_SYSTEM_ERROR_STATUS))
