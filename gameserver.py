# class to handle game commands

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
        return "<myxml>"

    # PURPOSE: Called for class construction
    # RETURNS: true for properly parsed command
    def parseCmd(self, cmd):
        if cmd == 'quit':
            print("quitCommandRecieved")
            self.gameContinues = False
        elif cmd == 'newgame':
            print("newGame")
        elif cmd == 'savegame':
            print("saveGame")
        elif cmd == 'loadgame':
            print("loadGame")
        elif cmd == 'listgames':
            print("listGames")
        elif cmd == 'newplayer':
            print("newPlayer")
        elif cmd == 'buildship':
            print("buildShip")
        elif cmd == 'moveship':
            print("moveShip")
        elif cmd == 'combatmove': # Per ship? All ships?
            print("combatMove")
        elif cmd == 'acceptdamage':
            print("acceptDamage")
        else:
            print("Not a legal command '", cmd, "'")
            return False

        return True
