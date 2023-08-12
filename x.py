import machine
import time

# Configure pin 17 as an output pin
pin17 = machine.Pin(17, machine.Pin.OUT)

try:
    # Send a 3.3V signal (HIGH) for 5 seconds
    pin17.on()
    time.sleep(5)
    
    # Turn off the signal
    pin17.off()

finally:
    # No need for cleanup in MicroPython on ESP32
    pass

