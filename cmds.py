#
# Make the construction of xml commands easier to use.
#

import sys
sys.path.append("/home/ahw/views/warpWar/test")

import XML2Py
import Py2XML

# A class to create xml commnds
# Does this really need to be a class? It seems like just using the namespace
# would be good enough?
class warpWarCmds():

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        print("create Cmd ... thingy")

    # PURPOSE: Create a new game string
    # RETURNS: string with xml
    def newGame(self, name):
        cmd  = { 'cmd' : {'cmd': "newgame", 'name': name} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the save string
    # RETURNS: string with xml
    def saveGame(self):
        cmd  = { 'cmd' : {'cmd': "savegame"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def restoreGame(self):
        cmd  = { 'cmd' : {'cmd': "restoregame"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def listGames(self):
        cmd  = { 'cmd' : {'cmd': "listgames"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def loadGame(self):
        cmd  = { 'cmd' : {'cmd': "loadgame"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the new player string
    # RETURNS: string with xml
    def newPlayer(self, name):
        cmd  = { 'cmd' : {'cmd': "newPlayer", 'name': name} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def playerLeave(self):
        cmd  = { 'cmd' : {'cmd': "playerleave"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def buildShip(self):
        cmd  = { 'cmd' : {'cmd': "buildship"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def moveShip(self):
        cmd  = { 'cmd' : {'cmd': "moveship"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def combatOrders(self):
        cmd  = { 'cmd' : {'cmd': "combatorders"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the XXX string
    # RETURNS: string with xml
    def acceptDamage(self):
        cmd  = { 'cmd' : {'cmd': "acceptdamage"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr

    # PURPOSE: Create the quit string
    # RETURNS: string with xml
    def quitGame(self):
        cmd  = { 'cmd' : {'cmd': "quit"} }
        xmlStr = Py2XML.Py2XML().parse(cmd, None)
        return xmlStr
