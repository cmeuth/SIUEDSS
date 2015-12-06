import time
import serial

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=19200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=0.5
)

ser.close()
ser.open()
if ser.isOpen():
	print "Serial is open"

# Variables for communication
char_read = ""
message = ""
i = 0
# Values that are generated here.
instruments = [
	'000A',	# Speed
	'0064',	# Voltage
	'001E',	# Current Draw
	'0000',	# Controller Temp 1
	'0000',	# Controller Temp 2
	'0000',	# Motor Temp
	'0000',	# State of Charge
	'0000',	# Throttle Position
	'0000',	# Regen Position
	'0000',	# Desired Current
	'0000',	# Desired Speed
	'0000',	# Target Current
	'0000',	# Drive State
	'0000',	# Fault 1 Latch
	'0000',	# Fault 1 Definition
	'0000',	# Fault 2 
	'0000',	# Fault 3
	'0000',	# Throttle Limit
	'0000'	# Regen Limit
]

while True:

#	while char_read != "\r":
	char_read =  ser.read( 1 )
#	message  =  ser.read( 1 )
		
#		print char_read
	message += char_read
	
	if char_read == "\r":
#		print message
		time.sleep(0.1)	
		if message == "1**?\r":
			print "All instrument Request"
#			message = ""
			# Echoes back orignal command and adds Line feed (\n or 0a)
			message = message.encode( "hex" )
			message += '0A'
			for x in instruments:
				message += ( x + '09' )
			message += '0D0A'
			print message			
			ser.write( message.decode( "hex" ) )
		
		elif message == "0F0!\r":
			print "Coast message received."

			message = message.encode( "hex" )
			message += '0A23000D0A'
#			print message
			ser.write( message.decode( "hex" ) )

		elif message == "000=F6\r":
                        print "Regen message received."

                        message = message.encode( "hex" )
                        message += '0A23000D0A'

                        ser.write( message.decode( "hex" ) )	
		message = ""
		print i
		i += 1

#	char_read = ""
#	time.sleep(0.1)

