#
# Make the construction of json commands easier to use.
#

import sys
sys.path.append("/home/ahw/views/warpWar/test")

import json

# A class to create json commnds
# Does this really need to be a class? It seems like just using the namespace
# would be good enough?
class warpWarCmds():

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        print("create Cmd ... thingy")

    # PURPOSE: test for server connectivity
    # RETURNS: string with json
    def ping(self):
        cmd  = { 'cmd' : {'cmd': "ping"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create a new game string
    # RETURNS: string with json
    def newGame(self, name):
        cmd  = { 'cmd' : {'cmd': "newgame", 'name': name} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the save string
    # RETURNS: string with json
    def saveGame(self):
        cmd  = { 'cmd' : {'cmd': "savegame"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def restoreGame(self):
        cmd  = { 'cmd' : {'cmd': "restoregame"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def listGames(self):
        cmd  = { 'cmd' : {'cmd': "listgames"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def loadGame(self):
        cmd  = { 'cmd' : {'cmd': "loadgame"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the new player string
    # RETURNS: string with json
    def newPlayer(self, name):
        cmd  = { 'cmd' : {'cmd': "newPlayer", 'name': name} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def playerLeave(self):
        cmd  = { 'cmd' : {'cmd': "playerleave"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def buildShip(self):
        cmd  = { 'cmd' : {'cmd': "buildship"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def moveShip(self, name, x, y):
        cmd  = { 'cmd' : {'cmd':"moveship", 'name':name, 'x':x, 'y':y} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the endmove string
    # RETURNS: string with json
    def endMove(self, name, x, y):
        cmd  = { 'cmd' : {'cmd':"endmove", 'player':name} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def combatOrders(self):
        cmd  = { 'cmd' : {'cmd': "combatorders"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with json
    def acceptDamage(self):
        cmd  = { 'cmd' : {'cmd': "acceptdamage"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the quit string
    # RETURNS: string with json
    def quitGame(self):
        cmd  = { 'cmd' : {'cmd': "quit"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr
