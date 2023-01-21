import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time
from sr_scanner import Scanner

CLIENT_NAME = "Elevator_Scanner"
MQTT_BROKER ="mqtt.eclipseprojects.io"
SCANNER_IP = "192.168.1.54"
SCANNER_PORT = 9004

# -----------------------------------------------------------------------------

def read_scanner(s):
    return s.read_code()

def mock_scanner():
    return int(uniform(1, 14))

# -----------------------------------------------------------------------------

client = mqtt.Client(CLIENT_NAME)
client.connect(MQTT_BROKER) 

# s = Scanner(SCANNER_IP, SCANNER_PORT)

try:

    while True:
        # carrier_number = read_scanner(s)
        carrier_number = mock_scanner()
        client.publish("ELEVATOR_CARRIER", f"{carrier_number}")
        print(f"Just published carrier {carrier_number} to topic ELEVATOR_CARRIER")
        time.sleep(5)

except KeyboardInterrupt:
    # s.__exit__()
    print("Done")