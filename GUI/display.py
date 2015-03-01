from Tkinter import *
import json

# Fonts
smallFont = ("Times", 14, "bold")
mediumFont = ("Times", 16, "bold")
largeFont = ("Times", 20, "bold")

class Application( Frame ):

	def say_hi( self ):
		print "Hello World!"

	def createWidgets( self ):

		# Global Declarations
		global speedText
		global voltageText
		global currentText
		global cruiseText
		global regenColor
		global throttleColor
		global directionColor
		
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

		# Cruise Control Display
                self.cruise = Label( self.left, text="Cruise Control: ", width=20, font= smallFont )
                self.cruise.grid( column=0, row=3, sticky=W )

                self.cruiseValue = Label( self.left, textvariable=cruiseText, width=20, font= smallFont )
                self.cruiseValue.grid( column=1, row=3, sticky=E )

		# Right Side
                self.right = LabelFrame( self, text="Options", font=mediumFont )
                self.right.grid( column=1, row=0, padx=10, pady=10, ipadx=0, ipady=0, sticky=NSEW )

		# Buttons - For future implementation as well as display for now
		# Regen button
		self.regen = Button( self.right, text="REGEN" )
		self.regen.grid( column=2, row=0, sticky=E )

		# Throttle  button
                self.throttle = Button( self.right, text="THROTTLE" )
                self.throttle.grid( column=2, row=1, sticky=E )

		# Direction  button
                self.direction = Button( self.right, text="DIRECTION" )
                self.direction.grid( column=2, row=2, sticky=E )


	def __init__( self, master=None ):
		Frame.__init__( self, master, width=800, height=480 )
		self.grid()
		self.createWidgets()
		self.after( 2000, update )

def update(  ):

                # Global Declarations
                global speedText
                global voltageText
                global currentText
                global cruiseText
                global regenColor
                global throttleColor
                global directionColor
		global root

		data = {}
#		try:
               	with open( "data.json") as file:
                       	data = json.load( file )

                speedText.set( data[ "speed" ] + " mph" )
      	        voltageText.set( data[ "voltage" ] + " V")
               	currentText.set( data[ "current" ] + " A")
		
		if data[ "cruise"] == "0":
			cruiseText.set( "Off")
		else:
                	cruiseText.set( data[ "cruise" ] )

		if data[ "regen" ] == "0":
			self.regen.configure(bg =  "red" )
		else:
			regenColor =  "green"

		if data[ "throttle" ] == "0":
       	                throttleColor = "red"
               	else:
                       	throttleColor = "green"

		if data[ "direction" ] == "0":
       	                directionColor =  "red" 
               	else:
                       	directionColor = "green"

#		except:
#			print "Error Opening JSON"
		
		if not first:	
                	app.after( 2000, update )
#		print speedText
		print throttleColor
                print "Updated"

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
cruiseText = StringVar()
regenColor = StringVar()
throttleColor = StringVar()
directionColor = StringVar()

update()
first = False
# Create class. Add widgets to Frame
app = Application( master = root )
#app.after( 2000, update )
app.mainloop()
root.destroy()

