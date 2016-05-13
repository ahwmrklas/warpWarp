# Main program for WarpWar
# More stuff will go here someday
# Right now there is no client/server
#
# Written with Python 3.4.2
#

# imports
from hexgrid import *
from tkinter import *
from xbm import TileContent
from dataModel import *
from samplegame import sampleGame
from overlay import *

# PURPOSE: Button handler. The Quit button
#          call this when "Quit" button clicked
# RETURNS: I don't know.
def exitProgram(tk):
    print("quitMain")
    tk.destroy()
    tk.quit()

# I don't like these. They don't seem very objecty
# Perhaps each of them should be a class?
def newGame():
    print("newGame")

# I don't like these. They don't seem very objecty
def openGame():
    print("openGame")

# I don't like these. They don't seem very objecty
def saveGame():
    print("saveGame")

# I don't like these. They don't seem very objecty
def aboutHelp():
    print("aboutHelp")

# I don't like these. They don't seem very objecty
def helpHelp():
    print("helpHelp")

# PURPOSE: Create menu GUI elements
# RETURNS: none
def addMenus(tk):
    menuBar = Menu(tk)

    fileMenu = Menu(menuBar)

    fileMenu.add_command(label="New", command=newGame)
    fileMenu.add_command(label="Open", command=openGame)
    fileMenu.add_command(label="Save", command=saveGame)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=lambda:exitProgram(tk))

    menuBar.add_cascade(label="File", menu=fileMenu)

    helpMenu = Menu(menuBar)
    helpMenu.add_command(label="About", command=aboutHelp)
    helpMenu.add_command(label="Help", command=helpHelp)

    menuBar.add_cascade(label="Help", menu=helpMenu)

    tk.config(menu=menuBar)


# PURPOSE: Just make a function out of the main code. It doesn't
#          seem right without that.
# RETURNS: ?? hmmm
def main():

    # Instance of tkinter to do GUI stuff
    tk = Tk()

    # menu bar
    addMenus(tk)

    # create a hex map that is the basis of our game display
    hexMap = HexagonalGrid(tk, scale = 20, grid_width=30, grid_height=20)

    # Locate the hexmap on the tkinter "grid"
    hexMap.grid(row=0, column=0, padx=10, pady=10)

    # Create a quit button (obviously to exit the program)
    quit = Button(tk, text = "Quit", command = lambda :exitProgram(tk))

    # Locate the button on the tkinter "grid"
    quit.grid(row=1, column=0)

    # display the whole hexMap.
    hexMap.drawGrid('blue')

    hexMap.setCell(4,4, fill='pink', content=TileContent.BASIC_SHIP)

    hexMap.drawObjects(DrawArray(30, 20, sampleGame['objects']))

    foo = GameInfo(hexMap.grid_width, hexMap.grid_height, ["Alex", "Rex"])

    # Let tkinter main loop run forever and handle input events
    tk.mainloop()


# Start the main function
if __name__ == "__main__":
   main()
