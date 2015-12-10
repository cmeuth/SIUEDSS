import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.UART as UART
import serial
import bluetooth
import time as t
import threading
import json

################### Function Calls ####################
def serial_comm(arg1, stop_event):

	global ser
	global coastFlag
	global regenFlag
	global accelerationFlag
	global throttleFlag
	global ignitionFlag
	global directionFlag
	global send_data
	global speed_value
	global voltage_value
	global current_value
	global driver_log
	global desired_torque
	global throttleEnable
	global ignitionEnable
	global directionEnable
	inst_read = [''] * 39
	char_read = ''

	print "We're in!"
	all_inst = "1**?\r" # Gets all instrumentation
	serial_message = "" # What is read from MC
	coast_command = "0F0!\r"
	regen_assign = "000<FFF6\r"
	acc_assign = "000<"
	throttle_assign = "302.7="
	ignition_assign = "302.b="
	direction_assign = "302.c="

	#
	# Main loop to continually check which messages to send to Motor Controller
	# If no cmonnads to be sent, the instrumentation is read and sent to the user.
	#
	while (not stop_event.is_set()):
		print "sending command"
		inst_read = [''] * 39

#		regenFlag = True
		if coastFlag:
		        ser.write( coast_command )
			t.sleep( 0.2 )
			ch = ser.read()
                        if len(ch) == 0:
                                driver_log = "Timeout Reached"
                        else:
				serial_message = ch
				serial_message += ser.read( 10 )
				print serial_message

				coastFlag = False
				driver_log = "Coast Command sent"

		elif regenFlag:
			
			ser.write( coast_command )
                        t.sleep( 0.1 )
                        ch = ser.read()
                        if len(ch) == 0:
                                driver_log = "Timeout Reached"
                        else:
                                serial_message = ch
                                serial_message += ser.read( 10 )
                                print serial_message

			ser.write( regen_assign )
			t.sleep( 0.2 )
			ch = ser.read()			
			if len(ch) == 0:
                                driver_log = "Timeout Reached"
                        else:
                                serial_message = ch
                                serial_message += ser.read( 13 )
	   	                print serial_message

				regenFlag = False
				driver_log = "Regen Command sent"

		elif accelerationFlag:
				
			acc_assign += desired_torque
				
			acc_assign += '\r'
		        ser.write( acc_assign )
			print acc_assign
			t.sleep( 0.2 )
			ch = ser.read()
                        if len(ch) == 0:
                                driver_log = "Timeout Reached"
                        else:
                                serial_message = ch
                                serial_message += ser.read( 13 )
                                print serial_message

                                accelerationFlag = False
                                driver_log = "New Torque Requested"

			print "New Acceleration command sent"
			acc_assign = "000<"

		elif throttleFlag:
			if throttleEnable:
				throttle_assign += "1\r"
			else:
				throttle_assign += "0\r"

                        ser.write( throttle_assign )

                        t.sleep( 0.2 )
                        ch = ser.read()
                        if len(ch) == 0:
                                driver_log = "Timeout Reached"
                        else:
                                serial_message = ch
                                serial_message += ser.read( 12 )
                                print serial_message

				if throttleEnable:
	                                driver_log = "Throttle Enabled"
				else:
	                                driver_log = "Throttle Disabled"

                        throttle_assign = "302.7="
#		        ser.write( serial_message )
			throttleFlag = False
			print "Throttle command sent"
		elif ignitionFlag:
                        if ignitionEnable:
                                ignition_assign += "1\r"
                        else:
                                ignition_assign += "0\r"

                        ser.write( ignition_assign )

                        t.sleep( 0.2 )
                        ch = ser.read()
                        if len(ch) == 0:
                                driver_log = "Timeout Reached"
                        else:
                                serial_message = ch
                                serial_message += ser.read( 12 )
                                print serial_message
	                        if ignitionEnable:
        	                        driver_log = "Ignition Enabled"
                	        else:
                        	        driver_log = "Ignition Disabled"
				ignitionFlag = False

                        ignition_assign = "302.b="
			print "Ignition command sent"
		elif directionFlag:
			if directionEnable:
                                direction_assign += "1\r"
                        else:
                                direction_assign += "0\r"

                        ser.write( direction_assign )

                        t.sleep( 0.2 )
                        ch = ser.read()
                        if len(ch) == 0:
                                driver_log = "Timeout Reached"
                        else:
                                serial_message = ch
                                serial_message += ser.read( 13 )
                                print serial_message
                                if directionEnable:
                                        driver_log = "Direction Set to Forward"
                                else:
                                        driver_log = "Direction Set to Reverse"
                                directionFlag = False

                        direction_assign = "302.c="
			directionFlag = False
			print "Direction command sent"
		else:
			t.sleep( 0.2 )
		        ser.write( all_inst )
			print "Instrumentation query sent"
			i = 1
			ch = ser.read( 6 )
			if len(ch) == 0:
				print "Timeout Reached"
			else:
#				inst_read[0] = ch
				for i in range( 39 ):
					if ( i % 2 == 1 ):
						inst_read[ i ] = ser.read( 1 ).encode( "hex" )
					else:
						inst_read[ i ] = ser.read( 2 ).encode( "hex" )
			
		
				print inst_read	
				#
				# Set Speed, Voltage, Current Draw Data
				#
				speed_value = str( int( inst_read[0], 16 ) )
				voltage_value = str( int( inst_read[2], 16 ) )
				current_value = str( int( inst_read[4],16  ) )

				print "Speed: " + speed_value

	print "Serial Finished"
#################### End of Functions Definition ####################

def main():

	# Open serial communication
	global ser
	global ser2
	ser.close()
	ser2.close()
	ser.open()
	ser2.open()

	# Start serial without bluetooth connection ( Testing purposes only )
#	if ser.isOpen() & ser2.isOpen():
#			print "Serial is open!"
#			t1 =  threading.Thread( target = serial_comm, args = ( ) )
#			t1.setDaemon( True )
#			t1.start()
#	else:
#			print "Serial failed"
#			sys.exit(0)

	# Open Serial Threads
#	t1 = threading.Thread( target = serial_read, args = ( ) )
#	t1.setDaemon( True )
#	t1.start()

#	t2 = threading.Thread( target = serial_read, args = ( ) )
#        t2.setDaemon( True )
#        t2.start()
	
	# GPIO Setup
	pLeft = "P9_11"
	pRight = "P9_13"
	pBrakeOut = "P9_15"
	pBrakeIn = "P8_15"
	pRunning = "P9_16"

	GPIO.setup( pLeft, GPIO.OUT ) # Left
	GPIO.setup( pRight, GPIO.OUT ) # Right
	GPIO.setup( pBrakeOut, GPIO.OUT ) # Brakes
	GPIO.setup( pRunning, GPIO.OUT ) # Running LED

	GPIO.setup( pBrakeIn, GPIO.IN ) # Brakes
	GPIO.add_event_detect( pBrakeIn, GPIO.BOTH )

	global hazards_on
	global turn_right
	global turn_left
	global brakes_on

	global throttleFlag
	global ignitionFlag
	global accelerationFlag
	global regenFlag
	global coastFlag
	global directionFlag

	global desired_torque
	global speed_value
	global voltage_value
	global current_value

	global throttleEnable
	global ignitionEnable
	global directionEnable

	throttleFlag = False
	ignitionFlag = False
	accelerationFlag = False
	regenFlag = False
	coastFlag = False
	directionFlag = False

	blink_counter = 0

	brakes_on = False
	first_loop = True

	# Turn on LED to signal on
	GPIO.output( pRunning, GPIO.HIGH )

	while True:
		
	
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

		# Start up Serial Communication
		if ser.isOpen() & ser2.isOpen():
                	        print "Serial is open!"
				ser.flushInput()
				ser.flushOutput()
				t1_stop = threading.Event()
        	                t1 =  threading.Thread( target = serial_comm, args = (1, t1_stop ) )
                	        t1.setDaemon( True )
                        	t1.start()
	        else:
        	                print "Serial failed"
                	        sys.exit(0)
		try:
	
			try:
				while True:
	
					# Bluetooth receive
					data = client_sock.recv(1024)
		
#					print data

					if len( data ) == 0 :break
					global send_data
					send_data = data.split(",")
	
					# Check for changes and set flags for Serial Commands/Queries				
					if not first_loop:
						if send_data[4] != previous_data[4] and not accelerationFlag:
							accelerationFlag = True	
#							print send_data[4]	
							desired_torque = hex( int( send_data[4] ) ).split('x')[1]
#							desired_torque = hex( send_data[4] ).split( 'x' )[1]
#							print desired_torque
							if len( desired_torque ) == 1:
								desired_torque = ( "000" + desired_torque )
							elif len( desired_torque )== 2:
                                                	        desired_torque = ( "00" + desired_torque )
							elif len( desired_torque )== 3:
        	                                                desired_torque = ( "0" + desired_torque )
#							print desired_torque
	
						if send_data[6] != previous_data[6]:
							if send_data[6] == "1":
								regenFlag = True
							else:
								coastFlag = True

						if send_data[7] != previous_data[7]:
							if send_data[7] == "1":
								directionEnable = True
							else:
								directionEnable = False
							directionFlag = True

						if send_data[8] != previous_data[8]:
							if send_data[8] == "1":
								ignitionEnable = True
							else:
								ignitionEnable = False
							ignitionFlag = True

						if send_data[9] != previous_data[9]:
							if send_data[9] == "1":
								throttleEnable = True
							else:
								throttleEnable = False
							throttleFlag = True

						if send_data[10] != previous_data[10]:
							if send_data[10] == "1":
								coastFlag = True

						send_data[11] = speed_value
						send_data[12] = voltage_value
						send_data[13] = current_value
					# Check Hazards
					if send_data[0] == "1":
						hazards_on = True
						print "Hazards on"
#						GPIO.output( pLeft, GPIO.HIGH )
#						GPIO.output( pRight, GPIO.HIGH )
					else:
#						print "Hazards off"
						hazards_on = False
						blink_counter = 0
						if not ( turn_right & turn_left ):
							GPIO.output( pLeft, GPIO.LOW )
							GPIO.output( pRight, GPIO.LOW )

					# Check Right Turn Signal
					if (send_data[1] == "1"):
						print "Right Signal on"
						if not hazards_on:
							turn_right = True
#							GPIO.output( pRight, GPIO.HIGH )
					elif hazards_on != True:
						turn_right = False
						blink_counter = 0
#						print "Right Signal off"
						GPIO.output( pRight, GPIO.LOW )

					#Check Left Turn Signal
					if (send_data[2] == "1") & (hazards_on != True):
						print "Left Signal on"
						if not hazards_on:
							turn_left = True
#							GPIO.output( pLeft, GPIO.HIGH )
					elif hazards_on != True:
						turn_left = False
						blink_counter = 0
#						print "Left Signal Off"
						GPIO.output( pLeft, GPIO.LOW )

					# Check Brakes
#					if GPIO.event_detected( pBrakeIn ):
					if GPIO.input( pBrakeIn):
						brakes_on = True
#						send_data[10] = "1"
						coastFlag = True
					else:
						brakes_on = False	

					# Blink signals accordingly
					if turn_right:
						if blink_counter < 10:
							GPIO.output( pRight, GPIO.HIGH )
						elif blink_counter < 20:
							GPIO.output( pRight, GPIO.LOW )
						else:
							blink_counter = 0
						blink_counter += 1

					if turn_left:
                                                if blink_counter < 10:
                                                        GPIO.output( pLeft, GPIO.HIGH )
                                                elif blink_counter < 20:
                                                        GPIO.output( pLeft, GPIO.LOW )
                                                else:
                                                        blink_counter = 0
                                                blink_counter += 1
						
					if hazards_on:
                                                if blink_counter < 10:
                                                        GPIO.output( pRight, GPIO.HIGH )
                                                        GPIO.output( pLeft, GPIO.HIGH )
                                                elif blink_counter < 20:
                                                        GPIO.output( pRight, GPIO.LOW )
                                                        GPIO.output( pLeft, GPIO.LOW )
                                                else:
                                                        blink_counter = 0
                                                blink_counter += 1
			

					if brakes_on:
#						print "Brakes on"
						GPIO.output( pBrakeOut, GPIO.HIGH )
					else:
#						print "No brake"
						GPIO.output( pBrakeOut, GPIO.LOW )

					# Set previous data
					previous_data = send_data
					first_loop = False
					
					# Change Driver's Log
					send_data[14] = driver_log
					print client_sock.send( ",".join( send_data ) )
#					client_sock.send( "Message received." )
				

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
		try:
			t1_stop.set()
			print "Serial Connection stopped."
		except:
			print "Error stopping serial."
if __name__=="__main__":

	# UART Setup
	UART.setup("UART1")
	ser = serial.Serial(	port = "/dev/ttyO1",
				baudrate = 19200,
				parity = serial.PARITY_NONE,
				stopbits = serial.STOPBITS_ONE,
				bytesize = serial.EIGHTBITS,
				timeout = 0.5
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
	desired_torque = ''
	
	speed_value = "2"
	voltage_value = "2"
	current_value = "2"	
	driver_log = "Welcome to Black Nova."

	throttleEnable = False
        ignitionEnable = False
        directionEnable = False

	# Start main loop
	main()
