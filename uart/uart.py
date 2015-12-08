import Adafruit_BBIO.UART as UART
import serial
import time as t

UART.setup("UART1")
UART.setup("UART2")
#i=0

ser = serial.Serial(
	port='/dev/ttyO1',
	baudrate=19200,
	parity=serial.PARITY_NONE,
#	startbits=serial.STARTBITS_ONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS#,
#	timeout=0
)

ser2 = serial.Serial(
        port='/dev/ttyO2',
        baudrate=19200,
        parity=serial.PARITY_NONE,
#       startbits=serial.STARTBITS_ONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS#,
#       timeout=0
)

ser.close()
#ser2.close()

#ser2.open()
ser.open()

if ser.isOpen() & ser2.isOpen():
	print "Serial open"
	print "Serial 2 open"
#	ser.flushInput()
#	ser.flushOutput()

	i = 0
	char_read = ""

	while True:

		ser.write( "312A2A3F0D312A2A3F0D0A".decode( "hex" ) )

		while char_read != "0a":
			char_read = ser.read( 1 ).encode( "hex" )
			print char_read

		char_read = ""
else:
	print "Serial Fail"
	sys.exit( 0 )
