import paho.mqtt.client as mqtt
import time

carrier_data = []
carrier_ids = []
serials = []

last_count = 0

def on_message(client, userdata, message):
    value = message.payload.decode("utf-8")
    print(f"Received {message.topic}: ", str(value))
    if message.topic == 'ELEVATOR_CARRIER':
        carrier_ids.append(value)
    else:
        serials.append(value)

    global last_count
    if len(carrier_ids) is len(serials) and len(serials) is not last_count:
        carrier_data.append((carrier_ids[-1], serials[-1]))
        last_count = last_count + 1

    # print(carrier_ids)
    # print(serials)
    print(carrier_data)


def on_message_carrier(client, userdata, message):
    print(f"Received {message.topic}: ", str(message.payload.decode("utf-8")))


MQTT_BROKER ="mqtt.eclipseprojects.io"

client = mqtt.Client("Serial_Station_01")
client.connect(MQTT_BROKER) 

client.subscribe("ELEVATOR_CARRIER")
client.subscribe("INKJET_SERIAL")
client.on_message=on_message

# Or pass a list of topics (and message levels)
# topics = ["ELEVATOR_CARRIER", "INKJET_SERIAL"]
# topics = [("ELEVATOR_CARRIER", 1), ("INKJET_SERIAL", 1)]
# client.subscribe(topics)

# Or use seperate callback functions like this
# client.message_callback_add('INKJET_SERIAL', on_message)
# client.message_callback_add('ELEVATOR_CARRIER', on_message_carrier)

# client.loop_start()
# time.sleep(30)
# client.loop_stop()

try:
    client.loop_forever()
    
except KeyboardInterrupt:
    print("Done")
