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

	# Variables
	GPIO.setup("P9_11", GPIO.IN)
	GPIO.add_event_detect("P9_11", GPIO.BOTH)
	GPIO.setup("P9_15", GPIO.OUT)
	global running
	speed = 0

	try:

		while True:
			t.sleep(1)
			if GPIO.input("P9_11"):
				speed = speed + 5
				print "Speed: %s" % speed
			else:
				if (speed > 0):
					speed = speed - 5
				print "Speed: %s" % speed

	except KeyboardInterrupt:

		GPIO.cleanup()
		print "Ending program"

if __name__ == "__main__":
	
	running = False
	main()
