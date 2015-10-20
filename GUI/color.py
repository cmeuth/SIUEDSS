from Tkinter import *

root = Tk()
global colour
global colourselection 
global count 
colour = ""
colourselection= ['red', 'blue']
count = 1

def start(parent):
    Tk.after(parent, 1000, change)

def change():
  	global colour 
	global colourselection
	global count 

	if colour == 'red':
		colour = 'blue'
	else:
		color = 'red'

	print change

	button.configure( bg = color )



button = Button(text = 'start', command = lambda: start(root))
button.pack()

root.mainloop()

