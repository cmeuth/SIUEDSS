import bluetooth
import time as t

def search():
	print "finding bluetooth devices..."

	devices = bluetooth.discover_devices( duration=2, lookup_names = True )
	return devices

def main():

	revC_addr = "00:19:0E:15:AD:EF"

	port = 1

	sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

	for x in range(0, 100):
#		try:
		sock.connect((revC_addr, port))
		sock.send("Hello!")
#		except Exception, e:
#			print str(e)
#			t.sleep(0.01)
	sock.close()
if __name__=="__main__":

	main()
