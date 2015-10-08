import Adafruit_BBIO.UART as UART
import serial
import time as t

UART.setup("UART2")
i = 0

ser = serial.Serial(
	port='/dev/ttyO0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=0
)

ser.close()
ser.open()
if ser.isOpen():
	print "Serial is open"
	ser.flushInput()
	ser.flushOutput()

ser.write("Hi")
while True:
	try:
		while ser.inWaiting() > 0:
			try:	
				print ser.readline()
			except:
				print "Nothing to Read"
				break
	except:
		print "Input error"
			
	ser.write( "Sup bro" )
