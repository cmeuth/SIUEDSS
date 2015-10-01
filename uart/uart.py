import Adafruit_BBIO.UART as UART
import serial
import time as t

UART.setup("UART2")
i = 0

ser = serial.Serial(port = "/dev/ttyO0",baudrate=9600 )

ser.close()
ser.open()
if ser.isOpen():
	while i < 10:
		print "Serial is open!"
		ser.write("Hello World!")
		print ser.read(1)
		print "Got Something"	
else:
	print "Serial Sucks!"
ser.close()
