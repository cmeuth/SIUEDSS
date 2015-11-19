import Adafruit_BBIO.GPIO as GPIO
import time as t
import threading

def blink_leds( led ):
	
	global running

	while running:
		GPIO.output( led, GPIO.HIGH )
		t.sleep( 0.5 )
		GPIO.output( led, GPIO.LOW )
		t.sleep( 0.5 )
	print "thread closed"

############### Function Definitions over #############

def main():
	print "Setting up GPIO"

	accUp = "P8_14"
	accDown = "P8_15"

	# Variables
	GPIO.setup( accUp, GPIO.IN )
	GPIO.setup( accDown, GPIO.IN )
#	GPIO.add_event_detect( accDown, GPIO.BOTH )
#	GPIO.setup( "P9_15", GPIO.OUT )
	global running
	speed = 50

	try:
		print "IN"
		while True:
			t.sleep(.1)
			if GPIO.input( accUp ):
				speed = speed + 5
				print "Speed: %s" % speed
			elif GPIO.input( accDown ):
				if (speed > 0):
					speed = speed - 5
				print "Speed: %s" % speed

	except KeyboardInterrupt:

		GPIO.cleanup()
		print "Ending program"

if __name__ == "__main__":
	
	running = False
	main()
