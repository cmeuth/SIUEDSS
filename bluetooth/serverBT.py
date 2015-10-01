import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial
import bluetooth
import time as t
import threading
import json
import pprint

################### Function Calls ####################
def flash_hazards( led1, led2 ):

        global hazards_on
        print "Hazard Thread open"
        while hazards_on:
                GPIO.output( led1, GPIO.HIGH )
                GPIO.output( led2, GPIO.HIGH )
                t.sleep( 0.5 )
                GPIO.output( led1, GPIO.LOW )
                GPIO.output( led2, GPIO.LOW )
                t.sleep( 0.5 )
        print "Hazard Thread Closed"

def left_signal( led ):

        global turn_left
	print "Left Thread open"
        while turn_left:
                GPIO.output( led, GPIO.HIGH )
                t.sleep( 0.5 )
                GPIO.output( led, GPIO.LOW )
                t.sleep( 0.5 )
        print "Left Thread Closed"

def right_signal( led ):

        global turn_right
        print "Right Thread open"
        while turn_right:
                GPIO.output( led, GPIO.HIGH )
                t.sleep( 0.5 )
                GPIO.output( led, GPIO.LOW )
                t.sleep( 0.5 )
        print "Right Thread Closed"

def serial_read():
	
#################### End of Functions Definition ####################

def main():

	# UART Setup
	UART.setup("UART2")
	ser = serial.Serial(port = "/dev/ttyO0",baudrate=9600 )

	ser.close()
	ser.open()
	if ser.isOpen():
                print "Serial is open!"
	else:
        	print "Serial failed"
		exit(0)
	# GPIO Setup
	GPIO.setup("P9_15", GPIO.OUT) # Brake
	GPIO.setup("P9_13", GPIO.OUT) # Left
	GPIO.setup("P9_11", GPIO.OUT) # Right
        global hazards_on
	global turn_right
	global turn_left

	# Bluetooth Setup
	print "Creating Bluetooth Server"
	server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		
	server_sock.bind(("", bluetooth.PORT_ANY))
	server_sock.listen( 1 )

	port = server_sock.getsockname()[1]

	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

	bluetooth.advertise_service( server_sock, "SIUEDDS",
			   service_id = uuid,
			   service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
			   profiles = [ bluetooth.SERIAL_PORT_PROFILE ]
			 )

	print "Waiting for connection on RFCOMM channel %d" % port
	client_sock, address = server_sock.accept()

	print "Accepted connection from ", address

	try:
		try:
			while True:

				data = client_sock.recv(1024)
				
				if len( data ) == 0 :break
				send_data = data.split(",")

#				if send_data[0] == "1":
#					if hazards_on != True:
#	                                       	hazards_on = True
#                                        	t1 = threading.Thread( target = flash_hazards, args = ( "P9_11","P9_13", ) )
#                                        	t1.setDaemon( True )
#                                        	t1.start()
#						GPIO.output("P9_11", GPIO.HIGH)
#	                                        GPIO.output("P9_13", GPIO.HIGH)
#
#                                else:
#                                        hazards_on = False
#                                        GPIO.output("P9_11", GPIO.LOW)
#                                        GPIO.output("P9_13", GPIO.LOW)

                                if send_data[0] == "1":
					hazards_on = True
                                        print "Hazards on"
                                        GPIO.output("P9_11", GPIO.HIGH)
                                        GPIO.output("P9_13", GPIO.HIGH)
                                else:
					print "Hazards off"
					hazards_on = False
                                        GPIO.output("P9_11", GPIO.LOW)
                                        GPIO.output("P9_13", GPIO.LOW)

				if (send_data[1] == "1") & (hazards_on != True):
					turn_right = True
                                        print "Right Signal on"
                                        GPIO.output("P9_11", GPIO.HIGH)
                                elif hazards_on != True:
					turn_right = False
					print "Right Signal off"
                                        GPIO.output("P9_11", GPIO.LOW)

                                if (send_data[2] == "1") & (hazards_on != True):
					turn_left = True
                                        print "Left Signal on"
                                        GPIO.output("P9_13", GPIO.HIGH)
                                elif hazards_on != True:
					turn_left = False
                                        print "Left Signal Off"
                                        GPIO.output("P9_13", GPIO.LOW)


				if send_data[3] == "1":
					print "Brakes on"
                                        GPIO.output("P9_15", GPIO.HIGH)
				else:
					print "No brake"
                                        GPIO.output("P9_15", GPIO.LOW)

				print "STATUS"
				print "Hazards: [%s]" % send_data[0]
				print "Right: [%s]" % send_data[1]
				print "Left: [%s]" % send_data[2]
				print "Brakes: [%s]" % send_data[3]
				print "Acceleration: [%s]" % send_data[4]
				client_sock.send( "Message Received" )
				ser.write("Bluetooth Transfer Occured")

		except IOError:
			pass

		print "Closing connection for no good reason"
		client_sock.close()
		server_sock.close()	

	except KeyboardInterrupt:
		
		client_sock.close()
		server_sock.close()
		GPIO.cleanup()
		ser.close()

	print "Connection closed."	
if __name__=="__main__":

	turn_right = False
	turn_left = False
	hazards_on = False
	main()
