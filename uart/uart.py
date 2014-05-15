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
ser2.close()

ser2.open()
ser.open()
if ser.isOpen() & ser2.isOpen():
	print "Serial open"
	print "Serial 2 open"
#	ser.flushInput()
#	ser.flushOutput()

	i = 0
	while i < 10:
		t1 = t.time()
		ser.write("Hello World")
		sex = ser2.read(i)
		t2 = t.time()
		print "Time elapsed: "
		print (t2 - t1)
		i = i + 1
#		print i
#		print sex
#		print sex.encode("hex")
		ser.close()
		ser2.close()
		ser.open()
		ser2.open()

ser2.close()
ser.close()
#while True:
#	try:
#		while ser.inWaiting() > 0:
#			try:	
#				print ser.readline()
#			except:
#				print "Nothing to Read"
#				break
#	except:
#		print "Input error"
#			
#	ser.write( "Sup bro" )
 
# Eventually, you'll want to clean up, but leave this commented for now, 
# as it doesn't work yet
#UART.cleanup()
