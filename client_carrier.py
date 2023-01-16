import paho.mqtt.client as mqtt 
from random import randrange, uniform
import time

MQTT_BROKER ="mqtt.eclipseprojects.io" 

client = mqtt.Client("Elevator_Scanner")
client.connect(MQTT_BROKER) 

def read_scanner():
    return int(uniform(1, 14))

try:

    while True:
        carrier_number = read_scanner()
        client.publish("ELEVATOR_CARRIER", f"{carrier_number}")
        print(f"Just published carrier {carrier_number} to topic ELEVATOR_CARRIER")
        time.sleep(1)

except KeyboardInterrupt:
    print("Done")