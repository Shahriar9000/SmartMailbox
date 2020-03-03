import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

def cleanAndExit():
    print "Cleaning..."
    GPIO.cleanup()
    print "Bye!"
    sys.exit()

GPIO.setwarnings(False)

hx = HX711(5,6)

hx.set_reading_format("LSB", "MSB")

hx.set_reference_unit(92)

hx.reset()
hx.tare()

endTime = time.time() + 1

while time.time() <= endTime:
    val = hx.get_weight(1)
    print(val)

cleanAndExit()
