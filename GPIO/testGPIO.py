import Adafruit_BBIO.GPIO as GPIO
import time as t

# Change this to the pin you want to test
pin = "P9_26"

GPIO.setup( pin, GPIO.IN)
GPIO.add_event_detect( pin, GPIO.BOTH )

while True:

#	# Uncomment to test a GPIO pin as an output
#	GPIO.output( pin, GPIO.HIGH )
#	t.sleep( 1 )
#	GPIO.output( pin, GPIO.LOW )
#	t.sleep( 1 )

#	#Uncomment to test an Input
	if GPIO.event_detected( pin ):
		print "CHANGE!!?!"

	if GPIO.input( pin ):
		print "Input on"
	else:
		print "Input off"

	t.sleep( 1 )
