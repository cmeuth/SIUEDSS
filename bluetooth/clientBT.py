import Adafruit_BBIO.GPIO as GPIO
import bluetooth
import time as t
import sys

def send_BT( data, socket ):
	socket.send(data)
	incoming = socket.recv(1024)
	print incoming

def main():

	# Bluetooth Variables
	revC_addr = "00:19:0E:15:AD:EF"
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	data = [ 0, 0, 0, 0, 0]
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
		if GPIO.event_detected("P9_11"):
			print "Hazards Change"
			if GPIO.input("P9_11"):
				data[0] = 1
			else:
				data[0] = 0
		
		if GPIO.event_detected("P9_12"):
                        print "Right Turn Signal"
                        if GPIO.input("P9_12"):
                                data[1] = 1
                        else:
                                data[1] = 0

		if GPIO.event_detected("P9_14"):
                        print "Left Turn Signal"
                        if GPIO.input("P9_14"):
                                data[2] = 1
                        else:
                                data[2] = 0

                if GPIO.input("P9_13"):
              		print "Brake change"
                        data[3] = 1
                else:
                        data[3] = 0

		if GPIO.input("P9_15"):
			data[4] = data[2] + 5
		else:
			if data[4] > 0:
				data[4] = data[4] - 5

		if len(data) == 0 : break
		send_data = ""
		for x in data:
			send_data += (str(x) + ",")
#		print "data to send %s" % data
#		print "send as %s" % send_data

		sock.send(send_data)
		incoming = sock.recv(1024)
		print incoming
		t.sleep(2)
	sock.close()
if __name__=="__main__":

	main()
