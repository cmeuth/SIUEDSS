import serial
import time as t

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

while True:

	tdata = ser.read()

	t.sleep(0.1)

	data_left = ser.inWaiting()

	tdata += ser.read( data_left )

	print tdata

	tdata = ''
