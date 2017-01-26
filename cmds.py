#
# Make the construction of xml commands easier to use.
#

import sys
sys.path.append("/home/ahw/views/warpWar/test")

import json

# A class to create xml commnds
# Does this really need to be a class? It seems like just using the namespace
# would be good enough?
class warpWarCmds():

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        print("create Cmd ... thingy")

    # PURPOSE: test for server connectivity
    # RETURNS: string with xml
    def ping(self):
        cmd  = { 'cmd' : {'cmd': "ping"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create a new game string
    # RETURNS: string with xml
    def newGame(self, name):
        cmd  = { 'cmd' : {'cmd': "newgame", 'name': name} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the save string
    # RETURNS: string with xml
    def saveGame(self):
        cmd  = { 'cmd' : {'cmd': "savegame"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def restoreGame(self):
        cmd  = { 'cmd' : {'cmd': "restoregame"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def listGames(self):
        cmd  = { 'cmd' : {'cmd': "listgames"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def loadGame(self):
        cmd  = { 'cmd' : {'cmd': "loadgame"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the new player string
    # RETURNS: string with xml
    def newPlayer(self, name):
        cmd  = { 'cmd' : {'cmd': "newPlayer", 'name': name} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def playerLeave(self):
        cmd  = { 'cmd' : {'cmd': "playerleave"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def buildShip(self):
        cmd  = { 'cmd' : {'cmd': "buildship"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def moveShip(self):
        cmd  = { 'cmd' : {'cmd': "moveship"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def combatOrders(self):
        cmd  = { 'cmd' : {'cmd': "combatorders"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def acceptDamage(self):
        cmd  = { 'cmd' : {'cmd': "acceptdamage"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr

    # PURPOSE: Create the quit string
    # RETURNS: string with xml
    def quitGame(self):
        cmd  = { 'cmd' : {'cmd': "quit"} }
        xmlStr = json.dumps(cmd, ensure_ascii=False)
        return xmlStr
