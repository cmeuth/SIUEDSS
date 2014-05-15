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
    if (count < 2 ):
        colour = colourselection[count]
        button.configure(bg = colour)
        count + 1
    else:
        colour = colourselection[count]
        button.configure(bg = colour)
        count = 1 
    start(root)



button = Button(text = 'start', command = lambda: start(root))
button.pack()

root.mainloop()

