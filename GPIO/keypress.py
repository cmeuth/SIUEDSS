from Tkinter import *

main = Tk()

CRDIT = [0,0,0,0,0]

def leftKey(event):
	if CRDIT[0]  == 1:
		CRDIT[0] = 0
	else:
		CRDIT[0] = 1

	print CRDIT

def rightKey(event):
	if CRDIT[1]  == 1:
                CRDIT[1] = 0
        else:
                CRDIT[1] = 1

	print CRDIT

def upKey(event):
        if CRDIT[2]  == 1:
                CRDIT[2] = 0
        else:
                CRDIT[2] = 1

	print CRDIT

def downKey(event):
        if CRDIT[3]  == 1:
                CRDIT[3] = 0
        else:
                CRDIT[3] = 1

	print CRDIT

def enterKey(event):
        if CRDIT[4]  == 1:
                CRDIT[4] = 0
        else:
                CRDIT[4] = 1
	
	print CRDIT

frame = Frame( main, width = 100, height = 100 )

main.bind( '<Left>', leftKey )
main.bind( '<Right>', rightKey )
main.bind( '<Up>', upKey )
main.bind( '<Down>', downKey )
main.bind( '<Return>', enterKey )
frame.pack()
main.mainloop()
