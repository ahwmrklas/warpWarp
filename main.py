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

# PURPOSE:
# RETURNS: list of objects at x,y
def findObjectsAt(objList, x, y):
    retList = []
    for obj in objList:
        if ( x == obj['location']['x'] and y == obj['location']['y']):
           retList.append(obj)
    return retList

# PURPOSE:
# RETURNS: Nothing ... but a return might be useful
def clickHex(tkRoot, x, y):
    print("Clicked on ", x, y, " Display info about hex")

    # Find all of the things located at x,y
    lists = tkRoot.game['objects']
    starList = lists['starList']
    thingList = lists['thingList']
    shipList = lists['shipList']
    starBaseList = lists['starBaseList']
    xyList = []
    xyList.append(findObjectsAt(starList, x, y))
    xyList.append(findObjectsAt(thingList, x, y))
    xyList.append(findObjectsAt(shipList, x, y))
    xyList.append(findObjectsAt(starBaseList, x, y))

    hexInfo(tkRoot, xyList)

# PURPOSE:
# RETURNS: hexMap handle
def initMap(tkRoot, game):

    dim = game['map']

    # create a hex map that is the basis of our game display
    hexMap = HexagonalGrid(tkRoot, scale = 20, grid_width=dim['width'],
                           grid_height=dim['height'])

    hexMap.setClickCallBack(clickHex, tkRoot)

    # Locate the hexmap on the tkinter "grid"
    hexMap.grid(row=0, column=0, padx=10, pady=10)

    # display the whole hexMap.
    hexMap.drawGrid('blue')

    return hexMap

# PURPOSE:
# RETURN: none
def updateMap(tkRoot, hexMap, game):

    dim = game['map']
    lists = game['objects']
    starList = lists['starList']
    thingList = lists['thingList']
    shipList = lists['shipList']
    starBaseList = lists['starBaseList']

    # Break up the objectlists into a 2D array. I don't like this
    # but for the moment it works
    objArray = DrawArray(dim['width'], dim['height'], game['objects'])

    hexMap.drawObjects(objArray)

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

    foo = GameInfo(hexMap.grid_width, hexMap.grid_height, sampleGame['playerList'])

    # Let tkinter main loop run forever and handle input events
    tkRoot.mainloop()


# Start the main function
if __name__ == "__main__":
   main()
