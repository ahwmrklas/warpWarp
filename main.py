# Main program for WarpWar
# More stuff will go here someday
# Right now there is no client/server
#
# Written with Python 3.4.2
#

# imports
from hexgrid import *
from tkinter import *
from tkinter import filedialog
from dataModel import *
from samplegame import sampleGame
from overlay import *
from hexinfo import *
from build import *
from move import *
from mapUtil import *
from connect import *
from cmds import warpWarCmds
import json
import getpass


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

    tmp = connect(tkRoot, tkRoot.playerName, "127.0.1.1", "12345")
    if (tmp is not None):
        tkRoot.hCon = tmp.result
        tkRoot.playerName = tmp.playerName

        sendJson = warpWarCmds().newPlayer(tkRoot.playerName, tkRoot.playerName)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        pt = playerTableGet(tkRoot.game, tkRoot.playerName)
        assert(pt)
        phaseMenu(tkRoot, tkRoot.game['state']['phase'], pt['phase'])
        updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# PURPOSE:
# RETURNS:
def newGame(tkRoot):
    print("newGame")
    if (tkRoot.hCon is not None):
        sendJson = warpWarCmds().newGame(tkRoot.playerName, "foo")
        print(" main sending: ", sendJson)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        # not the right place to update.
        # Send message? And that updates?
        pt = playerTableGet(tkRoot.game, tkRoot.playerName)
        assert(pt)
        phaseMenu(tkRoot, tkRoot.game['state']['phase'], pt['phase'])
        updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# PURPOSE:
# RETURNS:
def sendReady(tkRoot):
    print("readyMenu")
    if (tkRoot.hCon is not None):
        sendJson = warpWarCmds().ready(tkRoot.playerName, tkRoot.playerName)
        print(" main sending: ", sendJson)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        # not the right place to update.
        # Send message? And that updates?
        pt = playerTableGet(tkRoot.game, tkRoot.playerName)
        assert(pt)
        phaseMenu(tkRoot, tkRoot.game['state']['phase'], pt['phase'])
        updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# PURPOSE:
# RETURNS:
def buildShip(tkRoot, base):
    print("buildMenu")
    if (tkRoot.hCon is not None):
        buildResult = build(tkRoot, base)

    if (buildResult is not None):
        sendJson = warpWarCmds().buildShip(tkRoot.playerName, buildResult.ship, base)
        print(" main sending: ", sendJson)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        # not the right place to update.
        # Send message? And that updates?
        pt = playerTableGet(tkRoot.game, tkRoot.playerName)
        assert(pt)
        phaseMenu(tkRoot, tkRoot.game['state']['phase'], pt['phase'])
        updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# PURPOSE:
# RETURNS:
def refresh(tkRoot):
    print("refresh")
    if (tkRoot.hCon is not None):
        sendJson = warpWarCmds().ping(tkRoot.playerName)
        tkRoot.hCon.sendCmd(sendJson)
        resp = tkRoot.hCon.waitFor(5)
        tkRoot.game = json.loads(resp)

        pt = playerTableGet(tkRoot.game, tkRoot.playerName)
        assert(pt)
        phaseMenu(tkRoot, tkRoot.game['state']['phase'], pt['phase'])
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

#Do we want restrictions on when this can be called?
def loadGame(tkRoot):
    print("loadGame")
    #so we need to open a file select menu, filtering for .wwr
    #then we just parse the string to our dict.
    loadFileName = filedialog.askopenfilename(title = "Select file",filetypes = (("warpWar files","*.wwr"),("all files","*.*")))
    print (loadFileName)
    loadFile = open(loadFileName, 'r')
    gameString = loadFile.read()
    loadFile.close()
    gameDict = json.loads(gameString)

    #send the game to the server.
    sendJson = warpWarCmds().restoreGame(tkRoot.playerName, gameDict)
    print (sendJson)
    tkRoot.hCon.sendCmd(sendJson)
    resp = tkRoot.hCon.waitFor(5)
    tkRoot.game = json.loads(resp)

    pt = playerTableGet(tkRoot.game, tkRoot.playerName)
    assert(pt)
    phaseMenu(tkRoot, tkRoot.game['state']['phase'], pt['phase'])
    updateMap(tkRoot, tkRoot.hexMap, tkRoot.game)

# I don't like these. They don't seem very objecty
def saveGame(game):
    print("saveGame")
    #convert to a string, the same way we send it.
    #write to a .wwr file
    saveString = json.dumps(game, ensure_ascii=False)
    saveFileName = filedialog.asksaveasfilename(title = "Select file",filetypes = (("warpWar files","*.wwr"),("all files","*.*")))
    print (saveFileName)
    saveFile = open (saveFileName, 'w')
    saveFile.write(saveString)
    saveFile.close()


# I don't like these. They don't seem very objecty
def aboutHelp():
    print("aboutHelp")

# I don't like these. They don't seem very objecty
def helpHelp():
    print("helpHelp")

def updateMenu(tkRoot):
    #for the moment, we just call phasemenu
    pt = playerTableGet(tkRoot.game, tkRoot.playerName)
    assert(pt)
    phaseMenu(tkRoot, tkRoot.game['state']['phase'], pt['phase'])

# PURPOSE: Delete previous and set new, phase menu
# RETURNS: none
def phaseMenu(tkRoot, gamePhase, playerPhase):
    print("Phase:", gamePhase, ", PlayerPhase:", playerPhase)
    menuBar = tkRoot.cget("menu")
    print("bar ", menuBar)
    print("")
    menuBar = tkRoot.nametowidget(menuBar)
    if (len(menuBar.children.items()) > 2):
        menuBar.delete(3)

    phaseMenuObject = Menu(menuBar)

    if (playerPhase == 'waiting'):
        # Player is waiting on opponent. All they can do is refresh.
        phaseMenuObject.add_command(label="WAITING on opponent")
    elif (gamePhase == 'nil'):
        phaseMenuObject.add_command(label="New",
                              command=lambda:newGame(tkRoot))
        phaseMenuObject.add_command(label="Open",
                              command=lambda:loadGame(tkRoot))
        tkRoot.hexMap.setRightPrivateCallBack(None, None)
    elif (gamePhase == 'creating'):
        phaseMenuObject.add_command(label="Ready",
                              command=lambda:sendReady(tkRoot))
        tkRoot.hexMap.setRightPrivateCallBack(None, None)
    elif (gamePhase == 'build'):
        phaseMenuObject.add_command(label="Bases you own:")
        for base in tkRoot.game['objects']['starBaseList']:
            if (base['owner'] == tkRoot.playerName):
                labelString = "'%s'    BP left: %d" % (base['name'],
                        base['stockpile'])
                phaseMenuObject.add_command(label=labelString, 
                                            command=lambda:buildShip(tkRoot, base))

        phaseMenuObject.add_command(label="Ready",
                              command=lambda:sendReady(tkRoot))
        #TODO: enable the move right click stuff.
        tkRoot.hexMap.setRightPrivateCallBack(None, None)
    elif (gamePhase == 'move'):
        #we also need to determine if it is our turn to move
        for player in tkRoot.game['playerList']:
            if player['name'] == tkRoot.playerName:
                if player['phase'] == "move":
                    phaseMenuObject.add_command(label="Ships you own:")
                    private = [tkRoot, "", tkRoot.hexMap, tkRoot.hexMap.getLeftPrivateCallBack()]
                    for ship in tkRoot.game['objects']['shipList']:
                        if (ship['owner'] == tkRoot.playerName):
                            labelString = "'%s'    Moves left: %d/%d" % (ship['name'],
                                                                         ship['moves']['cur'],
                                                                         ship['PD']['cur'])
                            private[1] = ship['name']
                            moveCommand = menuMover(private,
                                                    ship['location']['x'],
                                                    ship['location']['y'],
                                                    ship['moves']['cur'])
                            phaseMenuObject.add_command(label=labelString, command=moveCommand)
                    phaseMenuObject.add_command(label="Ready",
                                          command=lambda:sendReady(tkRoot))
                    #enable the move right click stuff.
                    setupMovement(tkRoot.hexMap, tkRoot)
                else:
                    tkRoot.hexMap.setRightPrivateCallBack(None, None)
    else:
        print("BAD PHASE", gamePhase)
        gamePhase = ""
        phaseMenuObject.add_command(label="Connect",
                              command=lambda:connectServer(tkRoot))

    phaseMenuObject.add_separator()
    phaseMenuObject.add_command(label="Refresh", command=lambda:refresh(tkRoot))

    menuBar.add_cascade(label="Phase " + gamePhase, menu=phaseMenuObject)

    #bind event
    tkRoot.bind("<<updateMenu>>", 
            lambda event:phaseMenu(tkRoot, gamePhase, playerPhase))

# PURPOSE: Create menu GUI elements
# RETURNS: none
def addMenus(tkRoot):
    menuBar = Menu(tkRoot)
    print("winfo", menuBar.winfo_id())

    fileMenu = Menu(menuBar)
    print("filemenu", fileMenu)

    fileMenu.add_command(label="Connect", command=lambda:connectServer(tkRoot))
    fileMenu.add_command(label="New", command=lambda:newGame(tkRoot))
    fileMenu.add_command(label="Open", command=lambda:loadGame(tkRoot))
    fileMenu.add_command(label="Save", command=lambda:saveGame(tkRoot.game))
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
    phaseMenu(tkRoot, None, None)

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
    tkRoot.playerName = getpass.getuser()

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
