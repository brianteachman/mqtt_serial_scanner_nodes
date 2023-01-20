import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
from sr_scanner import SRScanner

MQTT_BROKER ="mqtt.eclipseprojects.io"
SCANNER_IP = "192.168.1.54"
SCANNER_PORT = 9004

# -----------------------------------------------------------------------------

def read_scanner():
    s = SRScanner(SCANNER_IP, SCANNER_PORT)
    return s.read_code()

def mock_scanner():
    return int(uniform(1, 14))

client = mqtt.Client("Elevator_Scanner")
client.connect(MQTT_BROKER) 

# -----------------------------------------------------------------------------

try:

    while True:
        carrier_number = mock_scanner()
        client.publish("ELEVATOR_CARRIER", f"{carrier_number}")
        print(f"Just published carrier {carrier_number} to topic ELEVATOR_CARRIER")
        time.sleep(5)

except KeyboardInterrupt:
    print("Done")