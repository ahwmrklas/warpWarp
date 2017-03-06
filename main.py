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

        sendJson = warpWarCmds().newPlayer(tkRoot.playerName)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)
        phaseMenu(tkRoot, tkRoot.game['state']['phase'])

# PURPOSE:
# RETURNS:
def newGame(tkRoot):
    print("newGame")
    if (tkRoot.hCon is not None):
        sendJson = warpWarCmds().newGame("foo")
        print(" main sending: ", sendJson)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        # not the right place to update.
        # Send message? And that updates?
        phaseMenu(tkRoot, tkRoot.game['state']['phase'])
        updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# PURPOSE:
# RETURNS:
def sendReady(tkRoot):
    print("readyMenu")
    if (tkRoot.hCon is not None):
        sendJson = warpWarCmds().ready(tkRoot.playerName)
        print(" main sending: ", sendJson)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        # not the right place to update.
        # Send message? And that updates?
        phaseMenu(tkRoot, tkRoot.game['state']['phase'])
        updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# PURPOSE:
# RETURNS:
def refresh(tkRoot):
    print("refresh")
    if (tkRoot.hCon is not None):
        sendJson = warpWarCmds().ping()
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        phaseMenu(tkRoot, tkRoot.game['state']['phase'])
        updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# PURPOSE:
# RETURNS:
def popupPlayers(tkRoot):
    popup = Menu(tkRoot, tearoff=0)
    for player in tkRoot.game['playerList'] :
        popup.add_command(label = player['name'] +
                           " " + player['phase'])
        print("player",
              player['name'],
              player['phase'],
             )

    try:
        popup.post(tkRoot.winfo_pointerx(), tkRoot.winfo_pointery())
    finally:
        popup.grab_set()
        pass

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

# PURPOSE: Delete previous and set new, phase menu
# RETURNS: none
def phaseMenu(tkRoot, phase):
    print("Phase:", phase)
    menuBar = tkRoot.cget("menu")
    print("bar ", menuBar)
    print("")
    menuBar = tkRoot.nametowidget(menuBar)
    if (len(menuBar.children.items()) > 2):
        menuBar.delete(3)

    phaseMenu = Menu(menuBar)

    if (phase == 'nil'):
        phaseMenu.add_command(label="New",
                              command=lambda:newGame(tkRoot))
        phaseMenu.add_command(label="Open",
                              command=openGame)
        tkRoot.hexMap.setRightPrivateCallBack(None, None)
    elif (phase == 'creating'):
        phaseMenu.add_command(label="Ready",
                              command=lambda:sendReady(tkRoot))
        tkRoot.hexMap.setRightPrivateCallBack(None, None)
    elif (phase == 'build'):
        phaseMenu.add_command(label="Ready",
                              command=lambda:sendReady(tkRoot))
        tkRoot.hexMap.setRightPrivateCallBack(None, None)
    elif (phase == 'move'):
        phaseMenu.add_command(label="Ready",
                              command=lambda:sendReady(tkRoot))
        #enable the move right click stuff.
        setupMovement(tkRoot.hexMap, tkRoot)
    else:
        print("BAD PHASE", phase)
        phase = ""
        phaseMenu.add_command(label="Connect",
                              command=lambda:connectServer(tkRoot))

    menuBar.add_cascade(label="Phase " + phase, menu=phaseMenu)

# PURPOSE: Create menu GUI elements
# RETURNS: none
def addMenus(tkRoot):
    menuBar = Menu(tkRoot)
    print("winfo", menuBar.winfo_id())

    fileMenu = Menu(menuBar)
    print("filemenu", fileMenu)

    fileMenu.add_command(label="Connect", command=lambda:connectServer(tkRoot))
    fileMenu.add_command(label="New", command=lambda:newGame(tkRoot))
    fileMenu.add_command(label="Open", command=openGame)
    fileMenu.add_command(label="Save", command=saveGame)
    fileMenu.add_separator()
    fileMenu.add_command(label="Refresh", command=lambda:refresh(tkRoot))
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=lambda:exitProgram(tkRoot))

    menuBar.add_cascade(label="File", menu=fileMenu)

    helpMenu = Menu(menuBar)
    helpMenu.add_command(label="About", command=aboutHelp)
    helpMenu.add_command(label="Help", command=helpHelp)
    print("helpMenu", helpMenu)

    menuBar.add_cascade(label="Help", menu=helpMenu)

    tkRoot.config(menu=menuBar)
    phaseMenu(tkRoot, None)

# PURPOSE: Just make a function out of the main code. It doesn't
#          seem right without that.
# RETURNS: ?? hmmm
def main():

    # Instance of tkinter to do GUI stuff
    tkRoot = Tk()
    tkRoot.title("WarpWar")
    tkRoot.hCon = None
    tkRoot.hexMap = None
    tkRoot.game = None
    tkRoot.playerName = 'dad' # fill this in programatically

    tkRoot.game = sampleGame

    # menu bar
    addMenus(tkRoot)

    tkRoot.mapFrame = Frame(tkRoot)
    tkRoot.hexMap = initMap(tkRoot,
                            tkRoot.game['map']['width'],
                            tkRoot.game['map']['height'])
    tkRoot.mapFrame.pack()

    tkRoot.buttonFrame = Frame(tkRoot)
    # Create a quit button (obviously to exit the program)
    # Locate the button on the tkinter "grid"
    tkRoot.quitButton = Button(tkRoot.buttonFrame, text = "Quit",
                  command = lambda :exitProgram(tkRoot))
    #tkRoot.quitButton.grid(row=1, column=0)
    tkRoot.quitButton.pack(side="left")

    tkRoot.playersButton = Button(tkRoot.buttonFrame, text = "Players",
                                  command = lambda :popupPlayers(tkRoot))
    #tkRoot.playersButton.grid(row=1, column=1)
    tkRoot.playersButton.pack(side="right")

    tkRoot.buttonFrame.pack()
    
    updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)


    # at the moment this does nothing valuable
    foo = GameInfo(tkRoot.hexMap.grid_width,
                   tkRoot.hexMap.grid_height,
                   tkRoot.game['playerList'])

    # Let tkinter main loop run forever and handle input events
    tkRoot.mainloop()


# Start the main function
if __name__ == "__main__":
   main()
