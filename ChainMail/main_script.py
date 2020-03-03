#! /usr/bin/python2
import time
import sys
import RPi.GPIO as GPIO
import time
import array as arr
import pymongo
from pymongo import MongoClient
import psycopg2
from Read_Barcode import call_barcode_reader

client = MongoClient('mongodb+srv://shly:ssyy7713@cluster0-jqcgs.mongodb.net/test?retryWrites=true&w=majority')
db = client['SmartMailBoxData']
collection = db['OrderedItems']
weight = collection.find_one()['weight']
print weight

EMULATE_HX711=False

referenceUnit = 256 

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

GPIO.setwarnings(False)

def cleanAndExit():
    print("Cleaning...")

    if not EMULATE_HX711:
        GPIO.cleanup()
    
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

# I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
# Still need to figure out why does it change.
# If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
# There is some code below to debug and log the order of the bits and the bytes.
# The first parameter is the order in which the bytes are used to build the "long" value.
# The second paramter is the order of the bits inside each byte.
# According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
hx.set_reading_format("MSB", "MSB")

# HOW TO CALCULATE THE REFFERENCE UNIT
# To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
# In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
# and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
# If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
#hx.set_reference_unit(113)
hx.set_reference_unit(referenceUnit)

hx.reset()

def begin_scale():
    hx.tare()

    print("Tare done! Add weight now...")

def weigh_item(t_val):
        
    # to use both channels, you'll need to tare them both
    #hx.tare_A()
    #hx.tare_B()

        weight_vals = arr.array('i', [0,0,0,0,0])
        index = 0
        sum = 0
        avg_val = 0
        target_val = t_val
        val = 0
        print(val)

        while (avg_val < target_val * 0.9) or (avg_val > target_val *  1.1):
            try:
            # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
            # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
            # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.
            
            # np_arr8_string = hx.get_np_arr8_string()
            # binary_string = hx.get_binary_string()
            # print binary_string + " " + np_arr8_string
            
            # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
                val = hx.get_weight(5)
                print(val)
                weight_vals[index] = val
                index += 1
                if(index == 5):
                    for i in weight_vals:
                        sum += i
                    print "SUM: "
                    print sum
                    avg_val = sum/5
                    print "AVG: "
                    print avg_val
                    sum = 0
                    index = 0

            # To get weight from both channels (if you have load cells hooked up 
            # to both channel A and B), do something like this
            #val_A = hx.get_weight_A(5)
            #val_B = hx.get_weight_B(5)
            #print "A: %s  B: %s" % ( val_A, val_B )

                hx.power_down()
                hx.power_up()
                time.sleep(0.1)

            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()

#servo
def begin_servo():
    servoPIN = 17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)

    p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWN with 50Hz
    p.start(2.5) # Initialization
    try:
        #ile True:
        #p.ChangeDutyCycle(5)
        #time.sleep(0.5)
        #p.ChangeDutyCycle(7.5)
        #time.sleep(0.5)
        #p.ChangeDutyCycle(10)
        #time.sleep(0.5)
        #p.ChangeDutyCycle(12.5)
        #time.sleep(0.5)
        #p.ChangeDutyCycle(10)
        #time.sleep(0.5)
        #p.ChangeDutyCycle(7.5)
        #time.sleep(0.5)
        #p.ChangeDutyCycle(5)
        #time.sleep(0.5)
        p.ChangeDutyCycle(10)
        time.sleep(1.5)
        p.ChangeDutyCycle(2.5)
        time.sleep(1.5)
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
            
cal_once = 0
barcode = 0
w = 0
#main script begins:
while(True):
    if(not(cal_once)):
        begin_scale()
        cal_once = 1
    
    barcode = call_barcode_reader()
    print "BARCODE:"
    print barcode    
    
    
    
    
    #Customer = db["Customer"]
   
    #Delivered_item = { "barcode" : barcode } 
    #customerquery = { "customer" : barcode }

    #print 
    #print customer_query

    #print Delivered_item['weight']
    #print customerquery['weight']

    #if Delivered_item != 0:

    #if customerquery != 0:

    #print collection.find_all()['barcode']    
    #w = collection.find_one()(barcode)
    #print "Weight:"
    #print w 
    if barcode == "60410021842":
        w = 28
    elif barcode == "722252121066":
        w = 68
    elif barcode == "96619281893":
        w = 24
    elif barcode == "111111111":
        w = 0
    print "WEIGHT"
    print w
    weigh_item(w)
    
    #DeliveryGuyAccess = DeliveryGuy.find(Delivered_item)

    #if DeliveryGuyAccess:
    #    weight = collection.find_one()['weight']
    #    weigh_item(weight)
    #else:
    #    CustomerAccess = Customer.find(Customer_query)
    #    if CustomerAccess:
    #        weight = collection.find_one()['weight']
    #        weigh_item(weight)
        
    begin_servo()


