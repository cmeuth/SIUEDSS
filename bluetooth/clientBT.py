import Adafruit_BBIO.GPIO as GPIO
import bluetooth
import time as t
import sys
import json
from pprint import pprint

def main():

	# Bluetooth Variables
	revC_addr = "00:19:0E:15:AD:EF"
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	data = [ 0, 0, 0, 0, 0, 0, 0, 0, 0]
	send_data = " "
	
	#GPIO Variables
	GPIO.setup("P9_11", GPIO.IN)	#Hazards
	GPIO.add_event_detect("P9_11", GPIO.BOTH)

	GPIO.setup("P9_12", GPIO.IN)	#Left
	GPIO.add_event_detect("P9_12", GPIO.BOTH)

	GPIO.setup("P9_13", GPIO.IN)	#Brakes
	GPIO.add_event_detect("P9_13", GPIO.BOTH)

	GPIO.setup("P9_14", GPIO.IN)	#Right
	GPIO.add_event_detect("P9_14", GPIO.BOTH)

	GPIO.setup("P9_15", GPIO.IN) # Accelerator

	GPIO.setup("P9_16", GPIO.IN) # Regen
	GPIO.add_event_detect("P9_16", GPIO.BOTH)

	GPIO.setup("P9_41", GPIO.IN) # Throttle
	GPIO.add_event_detect("P9_41", GPIO.BOTH)

	GPIO.setup("P9_42", GPIO.IN) # Direction
	GPIO.add_event_detect("P9_42", GPIO.BOTH)

	GPIO.setup("P9_21", GPIO.IN) # Cruise Control
	GPIO.add_event_detect("P9_21", GPIO.BOTH)

	service_matches = bluetooth.find_service( uuid = uuid, 
						  address = revC_addr 
						)
	if len(service_matches) == 0:
		print "Couldn't find other BBB"
		sys.exit(0)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print "Connecting to \"%s\" on %s" % (name, host)
	sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((host, port))

	print "Connected."
	while True:

		#Set Hazards
		if GPIO.event_detected("P9_11"):
			print "Hazards Change"
			if GPIO.input("P9_11"):
				data[0] = 1
			else:
				data[0] = 0
		
		#Set Right Turn Signal
		if GPIO.event_detected("P9_12"):
                        print "Right Turn Signal"
                        if GPIO.input("P9_12"):
                                data[1] = 1
                        else:
                                data[1] = 0

		#Set Left Turn Signal
		if GPIO.event_detected("P9_14"):
#                        print "Left Turn Signal"
                        if GPIO.input("P9_14"):
                                data[2] = 1
                        else:
                                data[2] = 0

		# Set Brake
                if GPIO.input("P9_13"):
#              		print "Brake change"
                        data[3] = 1
                else:
                        data[3] = 0

		# Set Acceleration
		if GPIO.input("P9_15"):
			data[4] = data[4] + 5
		else:
			if data[4] > 0:
				data[4] = data[4] - 5

		#Set Regen
                if GPIO.input("P9_16"):
			if data[5] == 0:
				data[5] = 1
			else:
				data[5] = 0		
		#Set Throttle
                if GPIO.input("P9_41"):
			if data[6] == 0:
				data[6] = 1
			else:
				data[6] = 0	
		#Set Direction
                if GPIO.input("P9_42"):
                        if data[7] == 0:
                                data[7] = 1
                        else:
                                data[7] = 0

		#Set Cruise Control Speed
                if GPIO.input("P9_21"):
                        if data[8] == 0:
                                data[8] = data[4]
                        else:
                                data[8] = 0
		# Send data
		if len(data) == 0 : break
		send_data = ""
		for x in data:
			send_data += (str(x) + ",")
#		print "data to send %s" % data
#		print "send as %s" % send_data

		sock.send(send_data)
		incoming = sock.recv(1024)
		print incoming
		t.sleep(0.1)
	sock.close()
if __name__=="__main__":

	main()
