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
    #          (moves to creating phase)
    # RETURNS: string with json
    def newGame(self, name):
        cmd  = { 'cmd' : {'cmd': "newgame", 'name': name} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: join an existing game with player name
    #          "gameName" is probably ignored right now
    # RETURNS: string with json
    def join(self, gameName, playerName):
        cmd  = { 'cmd' : {'cmd': "join",
                          'game': gameName, 'player': playerName} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the new player string
    #    DUPLICATE TODO FIXME XXX 
    # RETURNS: string with json
    def newPlayer(self, name):
        cmd  = { 'cmd' : {'cmd': "newplayer", 'name': name} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Generic ready command.
    #          Given player is ready for next phase
    # RETURNS: string with json
    def ready(self, player):
        cmd  = { 'cmd' : {'cmd': "ready", 'name': player} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Start the game
    #          (moves to build phase)
    # RETURNS: string with json
    def start(self):
        cmd  = { 'cmd' : {'cmd': "start"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the build ship string
    #       TODO    This is going to have many arguments!
    # RETURNS: string with json
    def buildShip(self):
        cmd  = { 'cmd' : {'cmd': "buildship"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the move ship string
    # RETURNS: string with json
    def moveShip(self, name, x, y):
        cmd  = { 'cmd' : {'cmd':"moveship", 'name':name, 'x':x, 'y':y} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the endmove string
    #    FIXME TODO -- duplicate of ready?
    # RETURNS: string with json
    def endMove(self, name, x, y):
        cmd  = { 'cmd' : {'cmd':"endmove", 'player':name} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the combat orders string
    #       TODO    This is going to have many arguments!
    #       TODO    For all involved ships?
    # RETURNS: string with json
    def combatOrders(self):
        cmd  = { 'cmd' : {'cmd': "combatorders"} }
        jsonStr = json.dumps(cmd, ensure_ascii=False)
        return jsonStr

    # PURPOSE: Create the XXX string
    #       TODO    This is going to have many arguments!
    #       TODO    For all involved ships?
    # Even if you received NO damage you should send this
    # command. It will be a trigger to know a player is done
    # with a battle and ready for the next one.
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

# The remaining functions might not be needed

    # PURPOSE: Create the XXX string
    #    TODO This is like quiting
    # RETURNS: string with json
    def playerLeave(self):
        cmd  = { 'cmd' : {'cmd': "playerleave"} }
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
