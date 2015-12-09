#
# Client Side: Steering Wheel
# Bluetooth Dongle: CSR 4.0
# Must run as root
#


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

# Logo

#
# GUI Class
#
class Application( Frame ):

	def updateButtons( self ):
		global regenColor
		global coastColor
		global throttleColor
		global directionColor
		global ignitionColor
		global directionText

	
                self.direction.configure( text = directionText )

		self.regen.configure( bg = regenColor )
		self.regen.configure( activebackground = regenColor )
		self.coast.configure( bg = coastColor )
		self.coast.configure( activebackground = coastColor )
		self.throttle.configure( bg = throttleColor )
		self.throttle.configure( activebackground = throttleColor )
		self.direction.configure( bg = directionColor )
		self.direction.configure( activebackground = directionColor )
		self.ignition.configure( bg = ignitionColor )
		self.ignition.configure( activebackground = ignitionColor )

        def __init__( self, master=None ):

		# Global Declarations
                global speedText
                global voltageText
                global currentText
                global accelerationText
                global cruiseText
		global directionText

                global regenColor
                global throttleColor
                global directionColor
                global ignitionColor
		global driver_log

                Frame.__init__( self, master )
                self.grid()
		self.master.title( "SIUE Solar Car Team" )
		
		logo = PhotoImage( file="../images/solar-banner.gif" ) 

		# Create Frames
		for r in range(6):
			self.master.rowconfigure( r, weight=1 )
		
		for c in range(5):
			self.master.columnconfigure( c, weight=1 )
		
		topFrame = Frame( master, bg="black" )
		topFrame.grid( row=0, column=0, rowspan = 1, columnspan = 5, sticky = W+E+N+S )

		statsFrame = Frame( master, bg="red" )
                statsFrame.grid( row=1, column=0, rowspan = 3, columnspan = 3, sticky = W+E+N+S )

		optionFrame = Frame( master, bg="red" )
                optionFrame.grid( row=1, column=3, rowspan = 3, columnspan = 2, sticky = W+E+N+S )
	
		logFrame = Frame( master, bg="black" )
                logFrame.grid( row=4, column=0, rowspan = 4, columnspan = 5, sticky = W+E+N+S )

#		logoLabel = Label( topFrame, image=logo )
		#	
		# Car Statistics
		#
		statsLabelFrame = LabelFrame( statsFrame, text="Car Statistics", font=mediumFont )
		statsLabelFrame.pack( fill=BOTH, expand=1, padx=5, pady=5 )

		# Speed Display
                self.speed = Label( statsLabelFrame, text="Speed: ", font= smallFont, width=20 )
                self.speed.grid( column=0, row=0, sticky=E )

                self.speedValue = Label( statsLabelFrame, textvariable=speedText, font= smallFont, width=20)
                self.speedValue.grid( column=1, row=0, sticky=W+E )

                # Voltage Display
                self.voltage = Label( statsLabelFrame, text="Voltage: ", font= smallFont, width=20 )
                self.voltage.grid( column=0, row=1, sticky=W )

                self.voltageValue = Label( statsLabelFrame, textvariable=voltageText, font= smallFont, width=20 )
                self.voltageValue.grid( column=1, row=1, sticky=W+E )

                # Current Draw Display
                self.current = Label( statsLabelFrame, text="Current Draw: ", font= smallFont, width=20 )
                self.current.grid( column=0, row=2, sticky=W )

                self.currentValue = Label( statsLabelFrame, textvariable=currentText, font= smallFont, width=20 )
                self.currentValue.grid( column=1, row=2, sticky=E )

                # Acceleration Display
                self.acceleration = Label( statsLabelFrame, text="Acceleration: ", font= smallFont, width=20 )
                self.acceleration.grid( column=0, row=3, sticky=W )

                self.accelerationValue = Label( statsLabelFrame, textvariable=accelerationText, font= smallFont, width=20 )
                self.accelerationValue.grid( column=1, row=3, sticky=E )

                # Cruise Control Display
                self.cruise = Label( statsLabelFrame, text="Cruise Control: ", font= smallFont, width=20 )
                self.cruise.grid( column=0, row=4, sticky=W )

                self.cruiseValue = Label( statsLabelFrame, textvariable=cruiseText, font= smallFont, width=20 )
                self.cruiseValue.grid( column=1, row=4, sticky=E )

		#
		# Car Options
		#
		optionsLabelFrame = LabelFrame( optionFrame, text="Options", font=mediumFont )
		optionsLabelFrame.pack( fill=BOTH, expand=1, padx=5, pady=5 )

		# Regen Button
                self.regen = Button( optionsLabelFrame, width=15, text="REGEN", font=smallFont, command=regenEnable )
                self.regen.grid( column=0, row=0, sticky=N )

		# Coast Button
                self.coast = Button( optionsLabelFrame, width=15, text="COAST", font=smallFont, command=lambda: rightKey('<Right>') )
                self.coast.grid( column=0, row=1, sticky=N )

                # Throttle Button
                self.throttle = Button( optionsLabelFrame, width=15, text="THROTTLE", font=smallFont, command=lambda: enterKey('<Return>') )
                self.throttle.grid( column=0, row=2, sticky=N, padx=100 )

                # Ignition Button
                self.ignition = Button( optionsLabelFrame, width=15, text="IGNITION", font=smallFont, command=lambda: downKey('<Down>') )
                self.ignition.grid( column=0, row=3, sticky=N )

		# Direction Button
                self.direction = Button( optionsLabelFrame, width=15, text="DIRECTION", font=smallFont, command=lambda: upKey('<Up>') )
                self.direction.grid( column=0, row=4, sticky=N )
	
		#
                # Top Frame
                #
                topLabel = Label( topFrame, image=logo, highlightthickness=0, borderwidth=0 )
		topLabel.image = logo
                topLabel.pack( )

		#
                # Driver's Log
                #
                logLabelFrame = LabelFrame( logFrame, text="Driver's Log", font=mediumFont )
                logLabelFrame.pack( fill=BOTH, expand=1, padx=5, pady=5 )
		
		# Lot Status
		statusLabel = Label( logLabelFrame, textvariable=driver_log, font=smallFont )
		statusLabel.pack( fill=BOTH, expand=1 )

		# After set time, call the update function
                self.after( 500, update )

#
# Functions for Keypresses. Handles Screen buttons.
# Must be bound to keys to root as defined in __init__
#

def regenEnable( ):

	global data
	global cruiseFlag

        if data[6]  == 1:
                data[6] = 0
        else:
		data[10] = 0
                data[6] = 1
		data[4] = 0
		cruiseFlag = False

# Hazards Control
def leftKey(event):
	global data

        if data[0] == 1:
                data[0] = 0
        else:
                data[0] = 1

# Coast Button
def rightKey(event):
        global data
	global cruiseFlag

        if data[10] == 1:
                data[10] = 0
        else:
                data[10] = 1
		data[6] = 0
		data[4] = 0
		cruiseFlag = False

# Direction
def upKey(event):
        global data
	global directionText

        if data[7] == 1:
                data[7] = 0
		directionText = "REVERSE"
        else:
                data[7] = 1
		directionText = "FORWARD"

# Ignition
def downKey(event):
        global data

        if data[8] == 1:
                data[8] = 0
        else:
                data[8] = 1

# Throttle Enable
def enterKey(event):
        global data

        if data[9] == 1:
                data[9] = 0
        elif data[8] == 1:
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
		global coastColor
                global root
		global data
		global cruiseSpeed
		global voltageValue
		global currentValue
		global driver_log
		# Values will have to be taken from Motor Controller
		# Place Holders
#		voltageValue = "100"
#		currentValue = "30"
		driver_log.set( data[14] )
		speedText.set( str( data[11] ) + " mph" )
                voltageText.set( str( data[12] ) + " V" )
                currentText.set( str( data[13] ) + " dA" )

		# Will need to be altered. Value will be used to determine amperage to tell MC to draw.
		accelerationText.set( str( data[4] ) + " dA" )

#                if data[5] == 0:
#                        cruiseText.set( "Off")
#			cruiseSpeed = 0
#                else:
#			# Used to lock in speed
#			if cruiseSpeed == 0:
#	                        cruiseText.set( data[4] )
#				cruiseSpeed = data[4]
#
#                if cruiseSpeed > data[4]:
#                        speedText.set( str( cruiseSpeed ) + " mph" )
#                else:
#                        speedText.set( str( data[4] ) + " mph" )


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

		if data[10] == 0:
			coastColor = "red"
		else:
			coastColor = "green"

#		print "Throttle: " + throttleColor
#		print "Regen: " + regenColor
#		print "Direction: " + directionColor

#               except:
#                       print "Error Opening JSON"

#                if not first:
		app.updateButtons()
                app.after( 500, update )
#               print speedText
#                print "Updated"

#
# This function 
#
def start():
	print "Main Loop Starting"
	global root
	try:
		t1 = threading.Thread( target = main, args = ( ) )
		t1.setDaemon = True
		t1.start()

		# Set Direction to Forward by default.
		upKey( "<Up>" )

	except KeyboardInterrupt:
		print "Main Loop Stopped."
#	app = Application( master = root )
#        app.after( 2000, update )
#        app.mainloop()
#        root.destroy()


#
# Main function for bluetooth, serial(to be added) and GPIO interfacing.
# 11/13/15: Brake functionality being moved to Server Side.
#
def main():

	# Pinout Variables
	pAccelerationUp = "P8_14"
	pAccelerationDown = "P8_15"
	pRegen = "P9_13"
	pLeft = "P9_26"
	pRight = "P9_24"
	pCruise = "P8_16"

	# Bluetooth Variables
	revC_addr = "00:19:0E:15:AD:EF"
	uuid =  "94f39d29-7d6d-437d-973b-fba39e49d4ee"
	send_data = " "

	# Global Variables
	global data	
	global cruiseSpeed
	global cruiseText
	global speedText
	global minimumSpeed
	global cruiseFlag
	global coastFlag
	global regenFlag
	global driver_log

	minimumSpeed = 0
	cruiseSpeed = 0
	desired_torque = 0

	#GPIO Variables
	GPIO.setup( pAccelerationUp, GPIO.IN ) #Acceleration Up
	GPIO.add_event_detect( pAccelerationUp, GPIO.BOTH )

	GPIO.setup( pAccelerationDown, GPIO.IN ) #Acceleration Down
        GPIO.add_event_detect( pAccelerationDown, GPIO.BOTH )

	GPIO.setup( pRegen, GPIO.IN )	# Regen
	GPIO.add_event_detect( pRegen, GPIO.BOTH )

	GPIO.setup( pLeft, GPIO.IN )	#Left
	GPIO.add_event_detect( pLeft, GPIO.BOTH )

	GPIO.setup( pRight, GPIO.IN )	#Right
	GPIO.add_event_detect( pRight, GPIO.BOTH )

	GPIO.setup( pCruise, GPIO.IN) # Cruise
	GPIO.add_event_detect( pCruise, GPIO.BOTH )

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

		# Regen
		if GPIO.event_detected( pRegen ):
#			print "Regen Change"
			if GPIO.input( pRegen ):
				regenEnable()
		
		#Set Left Turn Signal
		if GPIO.event_detected( pLeft ):
#                        print "Left Turn Signal"
                        if GPIO.input( pLeft ):
                                if data[1] == 0:
	        			data[1] = 1
					data[2] = 0
		                else:
        	                        data[1] = 0

		#Set Right Turn Signal
		if GPIO.event_detected( pRight ):
#                        print "Right Turn Signal"
                        if GPIO.input( pRight ):
 	                	if data[2] == 0:
					data[2] = 1
					data[1] = 0
				else:
                        		data[2] = 0

		# Set Cruise
		if GPIO.event_detected( pCruise ):
	                if GPIO.input( pCruise ):
				if not cruiseFlag:
					cruiseFlag = True
					cruiseSpeed = data[4]
				else:
					cruiseFlag = False		
#			cruiseFlag = not cruiseFlag
		
		if not cruiseFlag:
                        cruiseText.set( "Off")
                        cruiseSpeed = 0
#			speedText.set( str( data[4] ) + " mph" )
                else:
                        # Used to lock in speed
                        cruiseText.set( str( cruiseSpeed ) + " dA" )
#			speedText.set( str( cruiseSpeed ) + " mph" )
		
			

		# Set Acceleration. Throttle MUST be enabled.
		if data[9] == 1: 
			if GPIO.input( pAccelerationUp ):
				if data[4] < ( 500 + minimumSpeed) :
					data[4] = data[4] + 5
					if cruiseFlag:
						cruiseSpeed = cruiseSpeed + 5
			elif not cruiseFlag:
				if data[4] > 0:
					data[4] = data[4] - 5

			if ( cruiseFlag and GPIO.input( pAccelerationDown ) ):
#				speedText.set( str( cruiseSpeed ) + " mph" )
				if data[4] > 0:
					data[4] = data[4] -5
					cruiseSpeed = data[4]
		
		# Coast Select.
#		if data[10] == 1:
#			data[4] = 0
#			cruiseFlag = False

		if data[4] > 0:
			data[6] = 0
			data[10] = 0

		# Send data
		if len(data) == 0 : break
		send_data = ""

#		data[4] = str( hex( desired_torque ).split( 'x' )[1] )
#                if len(data[4] == 1):
#                        data[4] = "000" + data[4]
#                elif len(data[4] == 2):
#                        data[4] = "00" + data[4]
#                elif len(data[4] == 3):
#                        data[4] = "0" + data[4]

#                print data[4]
		for x in data:
			send_data += (str(x) + ",")
#		print "data to send %s" % data
#		print "send as %s" % send_data
#		print send_data

		sock.send(send_data)
		incoming = []
		incoming = sock.recv(1024).split(",")
		print incoming

		# Update UI based on info received	
		data[11] = incoming[11]
		data[12] = incoming[12]
		data[13] = incoming[13]
	
		data[14] = incoming[14]

		t.sleep(0.1)

	# Close GPIO and BT communication on exit
	GPIO.cleanup()
	sock.close()

if __name__=="__main__":

	# Root is the main Frame
	global root
	root = Tk()
	root.geometry( "800x480" ) # set to size on 7" Touch Screen

	# To Not Break : Check to see if still necessary
	first = True

	# Display Variables
	speedText = StringVar()
	voltageText = StringVar()
	currentText = StringVar()
	accelerationText = StringVar()
	cruiseText = StringVar()
	directionText = StringVar()

	coastColor = StringVar()
	regenColor = StringVar()
	throttleColor = StringVar()
	directionColor = StringVar()

	driver_log = StringVar()
	
	# Flags
	regenFlag = False
	coastFlag = False
	cruiseFlag = False

	# BT Data
	# 0 - Hazards
	# 1 - Left
	# 2 - Right
	# 3 - Brakes
	# 4 - Acceleration
	# 5 - Cruise
	# 6 - Regen
	# 7 - Direction
	# 8 - Ignition
	# 9 - Throttle
	# 10 - Coast
	# 11 - Speed
	# 12 - Voltage
	# 13 - Current Draw
	data = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '' ]
	# Create class. Add widgets to Frame
	app = Application( master = root )
	root.bind( '<Left>', leftKey )
	root.bind( '<Right>', rightKey )
	root.bind( '<Up>', upKey )
	root.bind( '<Down>', downKey )
	root.bind( '<Return>', enterKey )
#	# Uncomment to disable cursor.
#	root.config( cursor="none" )

	# Start 'Start' ( BT Connection ), then the mainloop of GUI
	app.after( 10, start )
	app.mainloop()
	root.destroy()

	print "Driver's Support deactivated."
