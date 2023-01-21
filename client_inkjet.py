import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from sr_scanner import Scanner

CLIENT_NAME = "Inkjet_Serial_Scanner"
MQTT_BROKER ="mqtt.eclipseprojects.io"
SCANNER_IP = "192.168.1.55"
SCANNER_PORT = 9004

# -----------------------------------------------------------------------------

def read_scanner(s):
    return s.read_code()

def mock_scanner():
    randNumber = int(uniform(2301150000, 2301150600))
    return str(randNumber) + 'W'

# -----------------------------------------------------------------------------

client = mqtt.Client(CLIENT_NAME)
client.connect(MQTT_BROKER)

# s = Scanner(SCANNER_IP, SCANNER_PORT)

try:

    while True:
        # carrier_number = read_scanner(s)
        serial_number = mock_scanner()
        client.publish("INKJET_SERIAL", serial_number)
        print(f"Just published serial {serial_number} to topic INKJET_SERIAL")
        time.sleep(8)

except KeyboardInterrupt:
    # s.__exit__()
    print("Done")
