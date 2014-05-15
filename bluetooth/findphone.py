import bluetooth
import time as t

def search():
	print "finding bluetooth Devices..."

	devices = bluetooth.discover_devices( duration=2, lookup_names=True )
	return devices

if __name__=="__main__":

	while True:
		results = search()

		print "found %d devices" % len( results )

		for addr, name in results:
			print " %s : %s" % (addr, name)
		
		t.sleep(5)
