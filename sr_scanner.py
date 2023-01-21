#import asyncio
import socket
from time import sleep

# Keyence Scanner ASCII Commands ------------------------------------------------------

"""
Error Format: ER,COMMAND,ERROR_CODE

Error Codes:
------------
00  Undefined command received
01  Mismatched command format (Invalid number of parameters)
02  The parameter 1 value exceeds the set value
03  The parameter 2 value exceeds the set value
04  Parameter 2 is not set in HEX (hexadecimal) code
05  Parameter 2 set in HEX (hexadecimal) code but exceeds the set value
10  There are 2 or more ! marks in the preset data, Preset data is incorrect
11  Area specification data is incorrect
12  Specified file does not exist
13  "mm" for the %Tmm-LON,bb command exceeds the setting range.
14  Communication cannot be checked with the %Tmm-KEYENCE command.
20  This command is not executable in the current status (execution error)
21  The buffer has overflowed, so commands cannot be executed
22  An error occurred while loading or saving parameters, so commands cannot be executed
23  Commands sent from RS-232C cannot be received because AutoID Network Navigator is being connected.
99  SR-1000 Series may be faulty. Please contact your nearest KEYENCE sales office
"""

# Read Serial Number
TRIGGER_INPUT_ON = b'LON\r'
TRIGGER_INPUT_OFF = b'LOFF\r'

REQUEST_SCANNER_VERSION = b'KEYENCE\r'

# Response: OK,FTUNE
REQUEST_FOCUS_ADJUSTMENT = b'FTUNE\r'

# Set the timing mode to "One-shot trigger" (one-shot signal trigger)
SET_ONESHOT_TRIGGER = b'WP,101,1\r'
# Check if one shot trigger is set
IS_ONESHOT_TRIGGER = b'RP,101\r'

SET_TIME_APPENDING = b'WP,300,1\r'
IS_TIME_APPENDING = b'RP,300,1\r'

""" Response: 
OK,NUM,a,b,c,d,e
    a: OK count
    b: NG count
    c: ERROR count
    d: STABLE count
    e: Trigger input count (0 to 65535)
"""
READING_HISTORY = b'NUM\r'

""" Response: 
OK,ERRSTAT,m
    m = None:       No error
        system:     System error
        update:     Update error
        cfg:        Set value error
        ip:         IP address duplication
        over:       Buffer overflow
        plc:        PLC link error
        profinet:   PROFINET error
        lua:        Script error
        hostconnect: Host connection erro
"""
GET_ERROR_STATUS = b'ERRSTAT\r'

# -----------------------------------------------------------------------------

"""
Class for Communication with an SR1000 Keyence Scanner
"""
class Scanner:

    def __init__(self, ip_addr, port, logger=None):
        self.ip = ip_addr
        self.port = port
        self.conn = None  # Socket Connection
        self.connected = False
        self.log = logger
        self._connect()

    def __enter__(self):
        return self

    def __exit__(self):
        self.conn.close()  # close the connection
        return True

    # Initiate a connection to the SR1000
    def _connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket Connection
        self.conn.settimeout(10)
        try:
            self.conn.connect((self.ip, self.port))  # connect to the server
            sleep(.1)
            # print(self._rx())
            self.connected = True
            print(f"Connected to {self.ip}:{self.port}")
        except socket.error as er:
            print(f"Connection Failed: {er}")

    def _tx(self, message):
        self.conn.sendall(message)  # send message

    def _rx(self):
        data = self.conn.recv(1024).decode()  # receive response
        return data
        
    # Send/Receive a Message
    def req(self, message):
        self._tx(message)  # send TCP message
        sleep(.1)
        data = self._rx()  # recieve TCP message
        return data

    # Send/Receive a Message
    def read_code(self):
        return str(self.req(TRIGGER_INPUT_ON))

    def has_error_type(self):
        return s.req(GET_ERROR_STATUS).replace('OK,ERRSTAT,', '')

# -----------------------------------------------------------------------------

if __name__ == '__main__':

    s = Scanner("192.168.1.54", 9004)

    try:

        while True:
            print(s.read_code())  # Fetch serial number
            sleep(1)

    except KeyboardInterrupt:
        print("Done")
