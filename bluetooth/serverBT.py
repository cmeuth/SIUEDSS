import bluetooth
import time as t

def search():
	print "finding bluetooth Devices..."

	devices = bluetooth.discover_devices( duration=2, lookup_names=True )
	return devices

def main():

	print "Creating Bluetooth Server"
	server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		
	server_sock.bind(("", bluetooth.PORT_ANY))
	server_sock.listen( 1 )

	port = server_sock.getsockname()[1]

	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

	bluetooth.advertise_service( server_sock, "SIUEDDS",
			   service_id = uuid,
			   service_classes = [ uuid, bluetooth.SERIAL_PORT_CLASS ],
			   profiles = [ bluetooth.SERIAL_PORT_PROFILE ]
			 )

	print "Waiting for connection on RFCOMM channel %d" % port
	client_sock, address = server_sock.accept()

	print "Accepted connection from ", address

	try:
		try:
			while True:

				data = client_sock.recv(1024)
				if len( data ) == 0 :break
				print "received [%s]" % data
				client_sock.send( data )

		except IOError:
			pass

		print "Closing connection for no good reason"
		client_sock.close()
		server_sock.close()	

	except KeyboardInterrupt:
		
		client_sock.close()
		server_sock.close()

	print "Connection closed."	
if __name__=="__main__":

	main()
