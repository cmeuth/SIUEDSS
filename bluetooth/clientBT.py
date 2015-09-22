import bluetooth
import time as t
import sys

def search():
	print "finding bluetooth devices..."

	devices = bluetooth.discover_devices( duration=2, lookup_names = True )
	return devices

def main():

	revC_addr = "00:19:0E:15:AD:EF"
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	
	service_matches = bluetooth.find_service( uuid = uuid, 
						  address = revC_addr 
						)
	if len(service_matches) == 0:
		print "Couldn't find other BBB"
		sys.exit(0)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print "Connecting to \"%s\" on %s" % (name, host)
	sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((host, port))

	print "Connected. Type Stuff"
	while True:
		data = "Hello"
		if len(data) == 0 : break
		sock.send(data)
		incoming = sock.recv(1024)
		print "Received [%s]" % incoming
	sock.close()
if __name__=="__main__":

	main()
