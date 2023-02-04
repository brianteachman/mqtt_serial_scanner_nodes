import paho.mqtt.client as mqtt
from random import randrange, uniform
import time
from sr1000 import Scanner
from dotenv import dotenv_values

config = dotenv_values()

MQTT_BROKER ="mqtt.eclipseprojects.io"

# -----------------------------------------------------------------------------

client = mqtt.Client("Inkjet_Serial_Scanner")
client.connect(MQTT_BROKER)

def read_scanner():
    s = Scanner(config["SR1000_SCANNER_IP"], config["SR1000_SCANNER_PORT"])
    return s.read_code()

def mock_scanner():
    randNumber = int(uniform(2301150000, 2301150600))
    return str(randNumber) + 'W'

try:

    while True:
        serial_number = mock_scanner()
        client.publish("INKJET_SERIAL", serial_number)
        print(f"Just published serial {serial_number} to topic INKJET_SERIAL")
        time.sleep(5)

except KeyboardInterrupt:
    print("Done")