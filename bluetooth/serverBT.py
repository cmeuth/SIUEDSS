import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial
import bluetooth
import time as t
import threading
import json

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

	global  ser
	global serial_send
	global serial_command
	while True:
		t.sleep(1)
		bytesToRead = ser.inWaiting()
		serial_send = ser.read( bytesToRead )
		if serial_send != '':
			print serial_send
                if serial_command != '':
                        ser.write( serial_command )

def serial_write():

        global  ser
        global serial_command
        while True:
                t.sleep(1)
                if serial_command != '':
                        ser.write( serial_command )

#################### End of Functions Definition ####################

def main():

	# Open serial communication
	global ser
	global ser2
	ser.close()
	ser2.close()
	ser.open()
	ser2.open()

	if ser.isOpen() & ser2.isOpen():
			print "Serial is open!"
	else:
			print "Serial failed"
			sys.exit(0)

	# Open Serial Threads
#	t1 = threading.Thread( target = serial_read, args = ( ) )
#	t1.setDaemon( True )
#	t1.start()

#	t2 = threading.Thread( target = serial_read, args = ( ) )
#        t2.setDaemon( True )
#        t2.start()
	
	# GPIO Setup
	pLeft = "P9_13"
	pRight = "P9_11"
	pBrake = "P9_15"

	GPIO.setup("P9_13", GPIO.OUT) # Left
	GPIO.setup("P9_11", GPIO.OUT) # Right
	GPIO.setup("P9_15", GPIO.OUT) # Brakes
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

				# Bluetooth receive
				data = client_sock.recv(1024)
	
				print data[0]

				ser.write( data )
				print "Serial Read: "
				sex = ser2.read( len( data ) )
				print sex

				print data
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

				# Check Hazards
				if send_data[0] == "1":
					hazards_on = True
					print "Hazards on"
					GPIO.output( pLeft, GPIO.HIGH )
					GPIO.output( pRight, GPIO.HIGH )
				else:
#					print "Hazards off"
#					hazards_on = False
					if not ( turn_right & turn_left ):
						GPIO.output( pLeft, GPIO.LOW )
						GPIO.output( pRight, GPIO.LOW )

				# Check Right Turn Signal
				if (send_data[1] == "1"):
					print "Right Signal on"
					if not hazards_on:
						turn_right = True
						GPIO.output( pRight, GPIO.HIGH )
				elif hazards_on != True:
					turn_right = False
#					print "Right Signal off"
					GPIO.output( pRight, GPIO.LOW )

				#Check Left Turn Signal
				if (send_data[2] == "1") & (hazards_on != True):
					print "Left Signal on"
					if not hazards_on:
						turn_left = True
						GPIO.output( pLeft, GPIO.HIGH )
				elif hazards_on != True:
					turn_left = False
#					print "Left Signal Off"
					GPIO.output( pLeft, GPIO.LOW )

				# Check Brakes
				if send_data[3] == "1":
#					print "Brakes on"
					GPIO.output( pBrake, GPIO.HIGH )
				else:
#					print "No brake"
					GPIO.output( pBrake, GPIO.LOW )

#                		if serial_command != '':
#                        		ser.write( serial_command.encode('hex') )
#				serial_send = ser.read( 5 )
#                		if serial_send != '':
#                		        print serial_send

				client_sock.send( ",".join( send_data ) )
#				client_sock.send( "Message received." )
				

		except IOError:
			print IOError
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

	# UART Setup
	UART.setup("UART1")
	ser = serial.Serial(	port = "/dev/ttyO1",
				baudrate = 19200,
				parity = serial.PARITY_NONE,
				stopbits = serial.STOPBITS_ONE,
				bytesize = serial.EIGHTBITS
			 )

	UART.setup("UART2")
        ser2 = serial.Serial(    port = "/dev/ttyO2",
                                baudrate = 19200,
                                parity = serial.PARITY_NONE,
                                stopbits = serial.STOPBITS_ONE,
                                bytesize = serial.EIGHTBITS
                         )

	# Global Variables
	turn_right = False
	turn_left = False
	hazards_on = False
	serial_command = ''
	serial_send = ''

	# Start main loop
	main()
