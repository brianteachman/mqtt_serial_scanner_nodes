import time
from machine import Pin
import sys

relay = Pin(0, machine.Pin.IN)
led = Pin("LED", machine.Pin.OUT)
led.value(0)

def led_on():
    led.value(1)

def led_off():
    led.value(0)


while True:
    
    # perform the requested action
    if relay.value():
        sys.stdout.write("CLOSED")
        led_on()
        print("Relay energized!")
    else:
        sys.stdout.write("OPEN")
        led_off()
        print("Relay not energized")