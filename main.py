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
from hexinfo import *
from move import *
from mapUtil import *

# PURPOSE: Button handler. The Quit button
#          call this when "Quit" button clicked
# RETURNS: I don't know.
def exitProgram(tkRoot):
    print("quitMain")
    tkRoot.destroy()
    tkRoot.quit()

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
def addMenus(tkRoot):
    menuBar = Menu(tkRoot)

    fileMenu = Menu(menuBar)

    fileMenu.add_command(label="New", command=newGame)
    fileMenu.add_command(label="Open", command=openGame)
    fileMenu.add_command(label="Save", command=saveGame)
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=lambda:exitProgram(tkRoot))

    menuBar.add_cascade(label="File", menu=fileMenu)

    helpMenu = Menu(menuBar)
    helpMenu.add_command(label="About", command=aboutHelp)
    helpMenu.add_command(label="Help", command=helpHelp)

    menuBar.add_cascade(label="Help", menu=helpMenu)

    tkRoot.config(menu=menuBar)



# PURPOSE: Just make a function out of the main code. It doesn't
#          seem right without that.
# RETURNS: ?? hmmm
def main():

    # Instance of tkinter to do GUI stuff
    tkRoot = Tk()

    # menu bar
    addMenus(tkRoot)

    tkRoot.game = sampleGame
    hexMap = initMap(tkRoot, sampleGame)

    # Create a quit button (obviously to exit the program)
    quit = Button(tkRoot, text = "Quit", command = lambda :exitProgram(tkRoot))

    # Locate the button on the tkinter "grid"
    quit.grid(row=1, column=0)
    
    updateMap(tkRoot, hexMap, sampleGame)

    setupMovement(hexMap, tkRoot)
    foo = GameInfo(hexMap.grid_width, hexMap.grid_height, sampleGame['playerList'])

    # Let tkinter main loop run forever and handle input events
    tkRoot.mainloop()


# Start the main function
if __name__ == "__main__":
   main()
