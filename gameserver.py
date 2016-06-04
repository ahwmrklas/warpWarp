# class to handle game commands

import sys
sys.path.append("/home/ahw/views/warpWar/test")

import XML2Py
import Py2XML
#from samplegame import sampleGame
import samplegame

# class to handle game commands
class gameserver:

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        self.gameContinues = True

    # PURPOSE: Have we received the quit command
    # RETURNS: true if no quit command yet
    def gameOn(self):
        return self.gameContinues

    # PURPOSE: Return the xml representing the entire game
    # RETURNS: game state as an xml string
    def gameXml(self):
        return Py2XML.Py2XML().parse(samplegame.sampleGame, None)

    # PURPOSE: Called for class construction
    # RETURNS: true for properly parsed command
    def parseCmd(self, cmd):
        if cmd == 'quit':
            print("quitCommandRecieved")
            self.gameContinues = False
        elif cmd == 'newgame':
            # What to do? Offer to save current game? NO! this is the server,
            # do as commanded
            # erase current game/dictionary
            # Start empty
            # Input? Would be list of options for game
            # Should we prevent this? Perhaps block it? Only permit it
            # if there is only one connected player?
            print("newGame")
        elif cmd == 'savegame':
            # Write file ... who is responsible for game save?
            # I Don't want to load/restore game that is stored on the server
            # ... well, I would like to but that API would be a pain.
            # I'd have to do all the directory I/O work. Remember the game
            # server has no UI. So I would read files and directories
            # off of the server and then let the client navigate, select and
            # choose save/load
            #
            # Server does nothing with saveGame. The client must save the game
            print("saveGame")
        elif cmd == 'loadgame':
            # Offer to save current game?
            # Bring up selection dialog
            # load game overwriting existing game
            #
            # Like, newGame check for permission.
            # Input? Would be an entire xml game
            # We should probably do some kind of validation but
            # this would just be pulling in the xml and
            # translating it to the dict.
            print("loadGame")
        elif cmd == 'listgames':
            # Because games are saved/restored on client ...
            # This would do nothing. Just like saveGame
            print("listGames")
        elif cmd == 'newplayer':
            # New player requests to join.
            # I guess we would look at the game state? Hmmm
            # What about a player joining a previously saved game?
            # Input? Player name and potentially player specific options
            # What player specific options? IP:port?
            print("newPlayer")
        elif cmd == 'playerleave':
            # Player is quiting
            # We could check for permission but I don't think so.
            # This is informational
            # Input? Player name? Some unique player key code for security?
            print("playerLeaving")
        elif cmd == 'buildship':
            # Now we get to fun stuff
            # Check for proper state to see if player permitted to build.
            # Validate a legal build. Does player have the money?
            # Input? ... this is a lot... The entire ship? We would have
            # to calculate the cost based on the options and validate it.
            # We would have to deduct the cost from the players total.
            # Of course need to see if it is a valid ship to begin with
            print("buildShip")
        elif cmd == 'moveship':
            # Input? ShipID, new location of ship? Movement vector?
            # Is it legal to move? (Proper turn sequence. Valid location on
            # map? Currently in combat? Does move cause combat? (meaning ship
            # halts immediately))
            # Deduct movement from ship
            print("moveShip")
        elif cmd == 'combatorders': # Per ship? All ships?
            # A combat instruction
            # Check for proper state. Are there existing orders?
            # Have all ships in combat been given orders?
            # Have all opponents ships in *this* combat been given orders?
            # Input? ShipID, combat command (fire, move, shields ...)
            print("combatOrders")
        elif cmd == 'acceptdamage':
            # Deduct combat damage
            # Input? ShipID, damage deducted from each component
            # Did they deduct enough damage?
            # Do they have more ships with damage to deduct?
            print("acceptDamage")
        else:
            print("Not a legal command '", cmd, "'")
            return False

        return True
