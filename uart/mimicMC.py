import threading
import time
import serial

def hex_fix( reading ):
	
	reading = hex( int( reading, 16 ) ).split('x')[1]

	if len( reading ) == 1:
		reading = ( "000" + reading )
	elif len( reading ) == 2:
                reading = ( "00" + reading )
	elif len( reading ) == 3:
                reading = ( "0" + reading )

	return reading

def generate_instrumentation():

	global speed
	global voltage
        global current
        global ignition
        global throttle
        global regen
        global coast
        global desired_torque
	global instruments
	global coastFlag
	global regenFlag
	global running

	rpm = 0
	v = 0
	while running:

		time.sleep(0.5)
		print rpm
		# Set torque
		instruments[9] = desired_torque		

		# Set Current Draw
		if int( current, 16 ) * 2 < int( desired_torque, 16 ):
			current = hex( int( current, 16 ) + 10 )
			rpm = rpm + 2
		elif current < desired_torque:
			current = hex( int( current, 16 ) + 5 )
			rpm = rpm + 1			
		elif current > desired_torque:
                	current = hex( int( current, 16 ) - 5 )
               	        rpm = rpm - 1
       	        elif int( current, 16 ) > int( desired_torque, 16 ) * 2:
        	        current = hex( int( current, 16 ) - 10 )
       	        	rpm = rpm - 2

		if desired_torque == "0000":
			current = "0000"		

		# Set Voltage
		if v < 0:
			voltage = hex( int( voltage, 16 ) + 1 )
			v = 0
		elif v == 2000:
			voltage = hex( int( voltage, 16 ) - 1 )
			v = 0
		if current > 0:
			v = v + 10
		if current > 250:
			v = v + 10
		if current < 0:
			v = v - 10		

		# Set Speed			
		if regenFlag:
			if speed > 1:
				speed = hex( int( speed, 16 ) - 2 )
			elif speed == 1:
				speed = hex( int( speed, 16 ) - 1 )

		if coastFlag:
			if speed > 0:
				speed = hex( int( speed, 16 ) - 1 )
		if rpm >= 3:
			speed = hex( int( speed, 16 ) + 1 )
			rpm = 0
		if rpm <= -2:
			rpm = 0
		if speed > 0:
			if current == 0:
				print "Speed down"
				speed = hex( int( speed, 16 ) - 1)
				
		voltage = hex_fix( voltage )
		current = hex_fix( current )
		speed = hex_fix( speed )
	
		instruments[0] = speed				
		instruments[1] = voltage
		instruments[2] = current
	
	print "Instrumentation Finished."

def main():
	# Variables for communication
	char_read = ""
	message = ""
	i = 0

	# Variables we will change.
        global speed
        global voltage
        global current
        global ignition
        global throttle
	global direction
        global regen
        global coast
        global desired_torque
	global instruments
	global regenFlag
	global coastFlag
	global running

	t1 = threading.Thread( target = generate_instrumentation, args = ( ) )
	t1.setDaemon( True )
	t1.start()

	try:
		while True:

			message = ""
			message = ser.read()
			time.sleep(0.1)
			data_left = ser.inWaiting()
			message += ser.read( data_left )
	
			if message == "1**?\r":
#				print instruments
#				message = ""
#				print message
				# Echoes back orignal command and adds Line feed (\n or 0a)
				message = message.encode( "hex" )
				message += '0A'
				for x in instruments:
					message += ( x + '09' )
				message += '0D0A'
#				print message			
				ser.write( message.decode( "hex" ) )
				print "All instrument Request"
				message = ""
			# Coast Message		
			elif message == "0F0!\r":
				message = message.encode( "hex" )
				message += '0A23000D0A'
#				print message
				ser.write( message.decode( "hex" ) )
				coastFlag = True
				regenFlag = False
				print "Coast message received."
				message = ""
			# Regen Message
			elif message == "000<FFF6\r":
				regenFlag = True
				coastFlag = False
				message = message.encode( "hex" )
                		message += '0A23000D0A'
				desired_torque = "0000"
#				print message
                		ser.write( message.decode( "hex" ) )	
                		print "Regen message received."
				message = ""
			# New Torque Message
			elif "000<" in message:
#				print message
			
				message = message.encode( "hex" )
			
				message += '0A23000D0A'
#				print message
	        		ser.write( message.decode( "hex" ) )
				print "New Torque Requested"
				desired_torque = message.decode( "hex" )[4:8]
#				print desired_torque
				regenFlag = False
				coastFlag = False
				message = ""

			# Set Throttle
			elif "302.7=" in message:
				message = message.encode( "hex" )

                                message += '0A23000D0A'
#                               print message
                                ser.write( message.decode( "hex" ) )
				print "Throttle Assigned."
				message = ""

			# Set Ignition
                        elif "302.b=" in message:
                                message = message.encode( "hex" )

                                message += '0A23000D0A'
#                               print message
                                ser.write( message.decode( "hex" ) )
				print "Ignition Assigned."
                                message = ""

			# Set Direction
                        elif "302.c=" in message:
                                message = message.encode( "hex" )

                                message += '0A23000D0A'
#                               print message
                                ser.write( message.decode( "hex" ) )
				print "Direction Assigned."
                                message = ""

#			print i
			i += 1
			if i % 100 == 0:
				print "Flushed"
				ser.flushInput()
				ser.flushOutput()

	except KeyboardInterrupt:
		running = False
		print "User Disabled."

if __name__=="__main__":

	# Variables we will change.
	speed = "0000"
	voltage = "0064"
	current = "0000"
	ignition = "0000"
	throttle = "0000"
	regen = "0000"
	coast = "0000"
	desired_torque = "0000"
	direction = "0000"
	
	regenFlag = False
	coastFlag = False
	running = True
	
	# Values that are generated here.
        instruments = [
                speed,          # Speed
                voltage,        # Voltage
                current,        # Current Draw
                '0000',         # Controller Temp 1
                '0000',         # Controller Temp 2
                '0000',         # Motor Temp
                '0000',         # State of Charge
                throttle,       # Throttle Position
                regen,          # Regen Position
                desired_torque, # Desired Current
                '0000',         # Desired Speed
                '0000',         # Target Current
                '0000',         # Drive State
                '0000',         # Fault 1 Latch
                '0000',         # Fault 1 Definition
                '0000',         # Fault 2 
                '0000',         # Fault 3
                '0000',         # Throttle Limit
                '0000'          # Regen Limit
        ]

	ser = serial.Serial(
        	port='/dev/ttyUSB0',
        	baudrate=19200,
        	parity=serial.PARITY_NONE,
        	stopbits=serial.STOPBITS_ONE,
        	bytesize=serial.EIGHTBITS#,
	#       timeout=0.5
	)
	
	ser.close()	
	ser.open()
	if ser.isOpen():
        	print "Serial is open"
		main()
	else:
		print "USB is not detected."
		
