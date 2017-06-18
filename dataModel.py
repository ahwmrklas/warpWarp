"""
Purpose: The python classes for the data model
This class should be designed with the JSON data that we eventually want to
send in mind.

map -- The dimensions of the game board. Two chars, x and y

players -- this is a list of players. Probably just their name, and how much
            money they have

objects -- This is a big one,
    stars -- A name and an X and Y location, nothing more
    wormholes -- This is a pair of stars
    ships
        type -- system or warp?
        stats -- everything that you payed a build point for
        stock -- what is on this ship? (warp ships can stock ships!)
        techLevel -- tech level at the time of creation
        moveLeft  -- how much movement is left for this ship? 0 when off turn
        location  -- Where is it
        owner -- who owns it?  
    bases
        location -- this is the name of a star
        ???
    anything else that goes on the map
        random events?

options -- for the moment, all this is is basic vs advanced

gameState -- This has a couple of components. phase of the turn, list of
            fighting ships, anything else we want to include
    turnCounter -- What game turn is it?
    techLevel   -- What is the tech level? (might not be needed)
    battleList  -- Which ships are in battle?

history -- we might want a history of every move that has been made

orders -- This is for storing the orders for ships in a battle

"""

class GameInfo():
    def __init__(self, width, height, playerNames, options=0):
        self.gameMap = (width, height) #X and Y dimensions of the board
        self.initOptions(options) #Game specific options
        self.initPlayers(playerNames) #set player specific information
        self.initObjects() #create objects and place them on the map
        self.initGameState() #set it to start of the game

    def initOptions(self, options):
        """
        This function should initialize any game options we decide to 
        implement

        This might include alternate rules, planet placement, and starting
        resources
        """
        if options == 0:
            #use the default settings
            return
        else:
            print ("Unrecognized game option")
            return

    def initPlayers(self, playerNames):
        """
        This initilizes the player list

        This also includes giving the players starting money
        """

        self.playerList = []

        for name in playerNames:
            self.playerList.append(Player(name))

    
    def initObjects(self):
        """
        This should create a list of objects, and place them on the board

        This includes all planets, bases, ships, and wormholes.
        """
        #TODO: actually do those things
        return

    def initGameState(self):
        """
        This sets the game state to to the begining of the game

        This sets the game turn counter to one.
        """
        self.turnCounter = 1


class Player():
    def __init__(self, name, resources=20, ships=[], bases=[]):
        self.name = name
        self.resources = resources
        self.shipList = ships
        self.baseList = bases


#
# (as of 06/11/17 above functions aren't doing anything useful)
# Collect "game" accessor functions here ... Maybe this isn't the correct
# location either but they are here now.
#

# PURPOSE: Return the player structure from the game
# RETURNS: player table
def playerTableGet(game, playerName):
    assert(game and playerName)
    for player in game['playerList'] :
        if (player['name'] == playerName):
            return player

    return None

# PURPOSE: create and return an empty game
#    FIXME TODO
#    I don't think this actually insantiates a new object.
# RETURNS: new empty game
def emptyGame():
    sampleGame = {
        'options': {
            'serverIp'  : "192.168.1.5",
            'mapSize'   : {'width':10, 'height':10},
            'startingBP': 20,
            'perTurnBP' :  5,
        },
        'state': {
            'turnNumber': 0,
            'phase': "nil",
            'activePlayer': "nil",
        },
        'map': {'width':10, 'height':10},
        'playerList': [
        ],
        'objects': {
            'starList': [
                {'name':"Alpha",
                 'type': "star",
                 'location': {'x':1, 'y':3},
                 'image':"alpha.png",
                 'owner':"nil",
                 'valueBP':3,
                 'visibility':[ {'player':"ahw",  'percent':100},
                                {'player':"bearda", 'percent':30},
                              ],
                },
            ],
            'thingList': [
                {'name':"AncientRelic",
                 'type': "special",
                 'location': {'x':4, 'y':7},
                 'image':"relic.png",
                 'owner':"nil",
                 'valueBP':0,
                 'visibility':[ {'player':"ahw",  'percent':100},
                                {'player':"bearda", 'percent':30},
                              ],
                },
            ],
            'shipList': [
            ],
            'starBaseList': [
                {'name': "Babylon 5",
                 'type': "base",
                 'location': {'x':4, 'y':8},
                 'image': "b_5.png",
                 'owner': "nil",
                 'stockpile': 15,
                },
            ],
            'warpLineList': [
                {'start': "Alpha", 'end': "Beta"},
                {'start': "Beta",  'end': "Alpha"},
            ],
        },
        'history': [
        ],
    }
    return sampleGame
