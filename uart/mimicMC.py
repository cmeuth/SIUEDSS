import time
import serial

ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=None
)
ser.close()
ser.open()
if ser.isOpen():
	print "Serial is open"
	ser.flushInput()
	ser.flushOutput()


while True:
	mimic = ''
	bytesToRead = ser.inWaiting()
	mimic = ser.read( bytesToRead )
	if mimic != '':
		print mimic

		time.sleep(0.5)
#		ser.write( "Got it" )
