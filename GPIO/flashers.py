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

	try:

		while True:
			if GPIO.event_detected("P9_11"):
				if GPIO.input("P9_11"):
					print "Hazards on"
					running = True
					t1 = threading.Thread( target = blink_leds, args = ( "P9_15", ) )
					t1.setDaemon( True )
					t1.start()
				else:
					running = False
					print "Hazards off"
					GPIO.output("P9_15", GPIO.LOW)	


	except KeyboardInterrupt:

		GPIO.cleanup()
		print "Ending program"

if __name__ == "__main__":
	
	running = False
	main()
