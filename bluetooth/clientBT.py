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
	GPIO.setup("P9_42", GPIO.IN)	#Hazards
	GPIO.add_event_detect("P9_42", GPIO.BOTH)

	GPIO.setup("P8_08", GPIO.IN)	#Brakes
#	GPIO.add_event_detect("P8_08", GPIO.BOTH)

	GPIO.setup("P8_15", GPIO.IN)	#Left
	GPIO.add_event_detect("P8_15", GPIO.BOTH)

	GPIO.setup("P8_14", GPIO.IN)	#Right
	GPIO.add_event_detect("P8_14", GPIO.BOTH)

	GPIO.setup("P8_07", GPIO.IN) # Accelerator

	GPIO.setup("P9_23", GPIO.IN) # Regen
#	GPIO.add_event_detect("P9_23", GPIO.BOTH)

	GPIO.setup("P9_21", GPIO.IN) # Throttle
#	GPIO.add_event_detect("P9_21", GPIO.BOTH)

	GPIO.setup("P9_27", GPIO.IN) # Direction
#	GPIO.add_event_detect("P9_27", GPIO.BOTH)

	GPIO.setup("P9_15", GPIO.IN) # Cruise Control
#	GPIO.add_event_detect("P9_15", GPIO.BOTH)

	GPIO.setup("P9_30", GPIO.IN) # Ignition
#        GPIO.add_event_detect("P9_30", GPIO.BOTH)

	while True:
		service_matches = bluetooth.find_service( uuid = uuid, 
						  address = revC_addr 
						)
	
		if len(service_matches) == 0:
			print "Couldn't find other BBB"
	#		sys.exit(0)
		else:
			break
		# Wait and try to connect again
		t.sleep(1)

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
		if GPIO.event_detected("P9_42"):
			print "Hazards Change"
			if GPIO.input("P9_42"):
				data[0] = 1
			else:
				data[0] = 0
		
		#Set Right Turn Signal
		if GPIO.event_detected("P8_15"):
                        print "Right Turn Signal"
                        if GPIO.input("P8_15"):
                                data[1] = 1
                        else:
                                data[1] = 0

		#Set Left Turn Signal
		if GPIO.event_detected("P8_14"):
#                        print "Left Turn Signal"
                        if GPIO.input("P8_14"):
                                data[2] = 1
                        else:
                                data[2] = 0

		# Set Brake
                if GPIO.input("P8_08"):
#              		print "Brake change"
                        data[3] = 1
                else:
                        data[3] = 0

		# Set Acceleration
		if GPIO.input("P8_07"):
			data[4] = data[4] + 5
		else:
			if data[4] > 0:
				data[4] = data[4] - 5

		#Set Regen
                if GPIO.input("P9_23"):
			if data[5] == 0:
				data[5] = 1
			else:
				data[5] = 0		
		#Set Throttle
                if GPIO.input("P9_21"):
			if data[6] == 0:
				data[6] = 1
			else:
				data[6] = 0	
		#Set Direction
                if GPIO.input("P9_27"):
                        if data[7] == 0:
                                data[7] = 1
                        else:
                                data[7] = 0

		#Set Cruise Control Speed
                if GPIO.input("P9_15"):
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
		incoming = []
		incoming = sock.recv(1024).split(",")
#		print incoming
		gui_info = {}

		# Build GUI file
		gui_info[ "hazards" ] = incoming[0] 
		gui_info[ "right" ] = incoming[1]
		gui_info[ "left" ] = incoming[2]
		gui_info[ "brakes" ] = incoming[3]
		gui_info[ "speed" ] = incoming[4]
		gui_info[ "regen" ] = incoming[5]
		gui_info[ "throttle" ] = incoming[6]
		gui_info[ "direction" ] = incoming[7]
		gui_info[ "cruise" ] = incoming[8]
		gui_info[ "voltage" ] = incoming[4]
		gui_info[ "current" ] = incoming[4]

		print gui_info

                # Write to GUI file
                with open('/home/debian/builds/SIUEDDS/GUI/data.json', 'r+') as file:
			file.truncate()
	                json.dump( gui_info, file )
#                       file.write( serial_command )
#                        print "File write complete"

#		print incoming
		t.sleep(0.1)
	sock.close()
if __name__=="__main__":

	main()
