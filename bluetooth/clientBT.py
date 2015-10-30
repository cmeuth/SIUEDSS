import Adafruit_BBIO.GPIO as GPIO
import bluetooth
import time as t
import sys
import json
import threading
from Tkinter import *

# Fonts. Section should be moved?
smallFont = ("Times", 14, "bold")
mediumFont = ("Times", 16, "bold")
largeFont = ("Times", 20, "bold")

#
# GUI Class
#
class Application( Frame ):

        def say_hi( self ):
                print "Hello World!"

        def createWidgets( self ):

                # Global Declarations
                global speedText
                global voltageText
                global currentText
		global accelerationText
                global cruiseText
                global regenColor
                global throttleColor
                global directionColor
		global ignitionColor

                # Left Side
                self.left = LabelFrame( self, text="Car Statistics", font=mediumFont )
                self.left.grid( column=0, row=0, padx=10, pady=10, ipadx=0, ipady=0, sticky=NSEW )

                # Speed Display
                self.speed = Label( self.left, text="Speed: ", width=20, font= smallFont )
                self.speed.grid( column=0, row=0, sticky=W )

                self.speedValue = Label( self.left, textvariable=speedText, width=20, font= smallFont)
                self.speedValue.grid( column=1, row=0, sticky=E )

                # Voltage Display
                self.voltage = Label( self.left, text="Voltage: ", width=20, font= smallFont )
                self.voltage.grid( column=0, row=1, sticky=W )

                self.voltageValue = Label( self.left, textvariable=voltageText, width=20, font= smallFont )
                self.voltageValue.grid( column=1, row=1, sticky=E )

                # Current Draw Display
                self.current = Label( self.left, text="Current Draw: ", width=20, font= smallFont )
                self.current.grid( column=0, row=2, sticky=W )

                self.currentValue = Label( self.left, textvariable=currentText, width=20, font= smallFont )
                self.currentValue.grid( column=1, row=2, sticky=E )
	
		# Acceleration Display
                self.acceleration = Label( self.left, text="Acceleration: ", width=20, font= smallFont )
                self.acceleration.grid( column=0, row=3, sticky=W )

                self.accelerationValue = Label( self.left, textvariable=accelerationText, width=20, font= smallFont )
                self.accelerationValue.grid( column=1, row=3, sticky=E )

                # Cruise Control Display
                self.cruise = Label( self.left, text="Cruise Control: ", width=20, font= smallFont )
                self.cruise.grid( column=0, row=4, sticky=W )

                self.cruiseValue = Label( self.left, textvariable=cruiseText, width=20, font= smallFont )
                self.cruiseValue.grid( column=1, row=4, sticky=E )

                # Right Side
                self.right = LabelFrame( self, text="Options", font=mediumFont )
                self.right.grid( column=1, row=0, padx=10, pady=10, ipadx=0, ipady=0, sticky=NSEW )

                # Buttons - For future implementation as well as display for now
                # Regen Button
                self.regen = Button( self.right, text="REGEN", command=lambda: rightKey('<Right>') )
                self.regen.grid( column=2, row=0, sticky=E )

                # Throttle Button
                self.throttle = Button( self.right, text="THROTTLE", command=lambda: enterKey('<Return>') )
                self.throttle.grid( column=2, row=1, sticky=E )

                # Direction Button
                self.direction = Button( self.right, text="DIRECTION", command=lambda: upKey('<Up>') )
                self.direction.grid( column=2, row=2, sticky=E )

		# Ignition Button
                self.ignition = Button( self.right, text="IGNITION", command=lambda: downKey('<Down>') )
                self.ignition.grid( column=2, row=3, sticky=E )

	def updateButtons( self ):
		global regenColor
		global throttleColor
		global directionColor
		global ignitionColor

		self.regen.configure( bg = regenColor )
		self.throttle.configure( bg = throttleColor )
		self.direction.configure( bg = directionColor )
		self.ignition.configure( bg = ignitionColor )

        def __init__( self, master=None ):
                Frame.__init__( self, master, width=800, height=480 )
                self.grid()
                self.createWidgets()
                self.after( 2000, update )

#
# Functions for Keypresses. Handles Screen buttons.
# Must be bound to keys to root as defined in __init__
#

# Cruise Control
def leftKey(event):
	global data

        if data[5]  == 1:
                data[5] = 0
        else:
                data[5] = 1

# Regen Enable
def rightKey(event):
        global data
	global minimumSpeed

        if data[6]  == 1:
                data[6] = 0
		minimumSpeed = 0
        else:
                data[6] = 1
		minimumSpeed = 50

# Direction
def upKey(event):
        global data

        if data[7]  == 1:
                data[7] = 0
        else:
                data[7] = 1

# Ignition
def downKey(event):
        global data

        if data[8]  == 1:
                data[8] = 0
        else:
                data[8] = 1

# Throttle Enable
def enterKey(event):
        global data

        if data[9]  == 1:
                data[9] = 0
        else:
                data[9] = 1


#
# Function to update properties for GUI
#
def update(  ):

                # Global Declarations
                global speedText
                global voltageText
                global currentText
		global accelerationText
                global cruiseText
                global regenColor
                global throttleColor
                global directionColor
		global ignitionColor
                global root
		global data
		global cruiseSpeed
		global voltageValue
		global currentValue
		# Values will have to be taken from Motor Controller
		# Place Holders
		voltageValue = "100"
		currentValue = "30"
		
#               try:
#                with open( "data.json") as file:
#                        data = json.load( file )

                voltageText.set( voltageValue + " V")
                currentText.set( currentValue + " A")
		accelerationText.set( str( data[4] * 2 ) + " %" )

                if data[5] == 0:
                        cruiseText.set( "Off")
			cruiseSpeed = 0
                else:
			# Used to lock in speed
			if cruiseSpeed == 0:
	                        cruiseText.set( data[4] )
				cruiseSpeed = data[4]

                if cruiseSpeed > data[4]:
                        speedText.set( str( cruiseSpeed ) + " mph" )
                else:
                        speedText.set( str( data[4] ) + " mph" )


                if data[6] == 0:
			
                        regenColor = "red"
                else:
                        regenColor =  "green"

                if data[9] == 0:
			throttleColor = "red"
                else:
                        throttleColor = "green"

                if data[7] == 0:
                        directionColor =  "red"
                else:
                        directionColor = "green"
		
		if data[8] == 0:
                        ignitionColor =  "red"
                else:
                        ignitionColor = "green"


		print "Throttle: " + throttleColor
		print "Regen: " + regenColor
		print "Direction: " + directionColor

#               except:
#                       print "Error Opening JSON"

#                if not first:
		app.updateButtons()
                app.after( 2000, update )
#               print speedText
                print "Updated"

#
#
#
def start():
	print "Main Loop Starting"
	global root
	try:
		t1 = threading.Thread( target = main, args = ( ) )
		t1.setDaemon = True
		t1.start()
	except KeyboardInterrupt:
		print "Main Loop Stopped."
#	app = Application( master = root )
#        app.after( 2000, update )
#        app.mainloop()
#        root.destroy()


#
# Main function for bluetooth, serial(to be added) and GPIO interfacing.
#
def main():

	# Pinout Variables
	pAcceleration = "P9_11"
	pHazard = "P9_13"
	pLeft = "P9_24"
	pRight = "P9_25"
	pBrake = "P9_26"

	# Bluetooth Variables
	revC_addr = "00:19:0E:15:AD:EF"
	uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	send_data = " "

	# Global Variables
	global data	
	global cruiseSpeed
	global minimumSpeed
	minimumSpeed = 0

	#GPIO Variables
	GPIO.setup( pAcceleration, GPIO.IN ) #Acceleration
	GPIO.add_event_detect( pAcceleration, GPIO.BOTH )

	GPIO.setup( pHazard, GPIO.IN )	# Hazards
	GPIO.add_event_detect( pHazard, GPIO.BOTH )

	GPIO.setup( pLeft, GPIO.IN )	#Left
	GPIO.add_event_detect( pLeft, GPIO.BOTH )

	GPIO.setup( pRight, GPIO.IN )	#Right
	GPIO.add_event_detect( pRight, GPIO.BOTH )

	GPIO.setup( pBrake, GPIO.IN) # Brakes
	GPIO.add_event_detect( pBrake, GPIO.BOTH )

	# Connect to other BBB. Wait for connection to open.
	while True:
		service_matches = bluetooth.find_service( uuid = uuid, 
						  address = revC_addr 
						)
	
		if len(service_matches) == 0:
			print "Couldn't find other BBB"
	#		sys.exit(0)
		else:
			break
		# Wait and try to connect again
		t.sleep(1)

	first_match = service_matches[0]
	port = first_match["port"]
	name = first_match["name"]
	host = first_match["host"]

	print "Connecting to \"%s\" on %s" % (name, host)
	sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	sock.connect((host, port))

	print "Connected."
	while True:

		#Set Hazards
		if GPIO.event_detected( pHazard ):
			print "Hazards Change"
			if GPIO.input( pHazard ):
				data[0] = 1
			else:
				data[0] = 0
		
		#Set Left Turn Signal
		if GPIO.event_detected( pLeft ):
#                        print "Left Turn Signal"
                        if GPIO.input( pLeft ):
                                data[1] = 1
                        else:
                                data[1] = 0

		#Set Right Turn Signal
		if GPIO.event_detected( pRight ):
#                        print "Right Turn Signal"
                        if GPIO.input( pRight ):
                                data[2] = 1
                        else:
                                data[2] = 0

		# Set Brake
                if GPIO.input( pBrake ):
#              		print "Brake change"
                        data[3] = 1
                else:
                        data[3] = 0

		# Set Acceleration
		if GPIO.input( pAcceleration ):
			if data[4] < ( 50 + minimumSpeed) :
				data[4] = data[4] + 1
		else:
			if data[4] > minimumSpeed:
				data[4] = data[4] - 1

		# Send data
		if len(data) == 0 : break
		send_data = ""
		for x in data:
			send_data += (str(x) + ",")
#		print "data to send %s" % data
#		print "send as %s" % send_data

		sock.send(send_data)
		incoming = []
		incoming = sock.recv(1024).split(",")
		print incoming

		t.sleep(0.1)

	# Close GPIO and BT communication on exit
	GPIO.cleanup()
	sock.close()

if __name__=="__main__":

	# Root is the main Frame
	global root
	root = Tk()
	root.geometry( "800x480" ) # set to size on 7" Touch Screen

	# To Not Break
	first = True

	# Display Variables
	speedText = StringVar()
	voltageText = StringVar()
	currentText = StringVar()
	accelerationText = StringVar()
	cruiseText = StringVar()
	regenColor = StringVar()
	throttleColor = StringVar()
	directionColor = StringVar()

	# BT Data
	data = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

#	update()
	first = False
	# Create class. Add widgets to Frame
	app = Application( master = root )
	root.bind( '<Left>', leftKey )
	root.bind( '<Right>', rightKey )
	root.bind( '<Up>', upKey )
	root.bind( '<Down>', downKey )
	root.bind( '<Return>', enterKey )
	app.after( 10, start )
	app.mainloop()
	root.destroy()
#	t1 = threading.Thread( target = start, args = ( ) )
#	t1.setDaemon = True
#	t1.start()

#	main()

	print "Driver's Support deactivated."
