import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from sr_scanner import SRScanner

MQTT_BROKER ="mqtt.eclipseprojects.io"
SCANNER_IP = "192.168.1.54"
SCANNER_PORT = 9004

# -----------------------------------------------------------------------------

client = mqtt.Client("Inkjet_Serial_Scanner")
client.connect(MQTT_BROKER)

s = SRScanner(SCANNER_IP, SCANNER_PORT)

def read_scanner():
    return s.read_code()

def mock_scanner():
    randNumber = int(uniform(2301150000, 2301150600))
    return str(randNumber) + 'W'

try:

    while True:
        serial_number = mock_scanner()
        client.publish("INKJET_SERIAL", serial_number)
        print(f"Just published serial {serial_number} to topic INKJET_SERIAL")
        time.sleep(1)

except KeyboardInterrupt:
    print("Done")