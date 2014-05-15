import bluetooth
import time as t

def search():
	print "finding bluetooth Devices..."

	devices = bluetooth.discover_devices( duration=2, lookup_names=True )
	return devices

def main():

	print "Creating Bluetooth Server"
	server_sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		
	port = 1
	server_sock.bind(("", port))
	server_sock.listen( 1 )

	client_sock, address = server_sock.accept()

	print "Accepted connection from ", address

	data = client_sock.recv(1024)
	print "received [%s]" % data

	client_sock.close()
	server_sock.close()	

	print "Connection closed."	
if __name__=="__main__":

	main()
