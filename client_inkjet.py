import paho.mqtt.client as mqtt
from random import randrange, uniform
import time

MQTT_BROKER ="mqtt.eclipseprojects.io"

client = mqtt.Client("Inkjet_Serial_Scanner")
client.connect(MQTT_BROKER)

def read_scanner():
    randNumber = int(uniform(2301150000, 2301150600))
    return str(randNumber) + 'W'

try:

    while True:
        serial_number = read_scanner()
        client.publish("INKJET_SERIAL", serial_number)
        print(f"Just published serial {serial_number} to topic INKJET_SERIAL")
        time.sleep(1)

except KeyboardInterrupt:
    print("Done")