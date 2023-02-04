import paho.mqtt.client as mqtt 
from random import randrange, uniform
from time import sleep
from sr1000 import Scanner
from dotenv import dotenv_values

config = dotenv_values()

MQTT_BROKER ="mqtt.eclipseprojects.io"

# -----------------------------------------------------------------------------

def read_scanner():
    s = Scanner(config["SR1000_SCANNER_IP"], config["SR1000_SCANNER_PORT"])
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
        sleep(5)

except KeyboardInterrupt:
    print("Done")