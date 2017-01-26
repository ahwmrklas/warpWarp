# Main program for WarpWar
# More stuff will go here someday
# Right now there is no client/server
#
# Written with Python 3.4.2
#

# imports
from hexgrid import *
from tkinter import *
from dataModel import *
from samplegame import sampleGame
from overlay import *
from hexinfo import *
from move import *
from mapUtil import *
from connect import *
from cmds import warpWarCmds
import json


# PURPOSE: Button handler. The Quit button
#          call this when "Quit" button clicked
# RETURNS: I don't know.
def exitProgram(tkRoot):
    print("quitMain")
    if (tkRoot.hCon is not None):
        tkRoot.hCon.quitCmd()
    tkRoot.destroy()
    tkRoot.quit()

# I don't like these. They don't seem very objecty
# Perhaps each of them should be a class?
def connectServer(tkRoot):
    print("connectServer")
    if (tkRoot.hCon is not None):
        tkRoot.hCon.quitCmd()
    tmp = connect(tkRoot, "silver", "12345")
    if (tmp is not None):
        tkRoot.hCon = tmp.result

def newGame(tkRoot):
    print("newGame")
    if (tkRoot.hCon is not None):
        sendXml = warpWarCmds().newGame("foo")
        print(" main sending: ", sendXml)
        tkRoot.hCon.sendCmd(sendXml)
        resp = tkRoot.hCon.waitFor(5)

    root = json.loads(resp)
    print("root")
    print(root)

    # not the right place to update.
    # Send message? And that updates?
    updateMap(tkRoot, tkRoot.hexMap, root)


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

    fileMenu.add_command(label="Connect", command=lambda:connectServer(tkRoot))
    fileMenu.add_command(label="New", command=lambda:newGame(tkRoot))
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
    tkRoot.hCon = None
    tkRoot.hexMap = None
    tkRoot.game = None

    # menu bar
    addMenus(tkRoot)

    tkRoot.game = sampleGame
    tkRoot.hexMap = initMap(tkRoot, sampleGame)

    # Create a quit button (obviously to exit the program)
    quit = Button(tkRoot, text = "Quit", command = lambda :exitProgram(tkRoot))

    # Locate the button on the tkinter "grid"
    quit.grid(row=1, column=0)
    
    updateMap(tkRoot, tkRoot.hexMap, sampleGame)

    setupMovement(tkRoot.hexMap, tkRoot)
    foo = GameInfo(tkRoot.hexMap.grid_width,
                   tkRoot.hexMap.grid_height,
                   sampleGame['playerList'])

    # Let tkinter main loop run forever and handle input events
    tkRoot.mainloop()


# Start the main function
if __name__ == "__main__":
   main()
