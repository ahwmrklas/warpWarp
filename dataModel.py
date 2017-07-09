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

# PURPOSE: look up ship name in game ship list
# RETURNS: entry of ship
def findShip(game, shipName):
   for ship in game['objects']['shipList']:
        if ship['name'] == shipName:
            return ship
   return None

# PURPOSE: Return the player structure from the game
# RETURNS: player table
def playerTableGet(game, playerName):
    assert(game and playerName)
    for player in game['playerList'] :
        if (player['name'] == playerName):
            return player

    return None

# PURPOSE:for sorted() key function
# RETURNS: key for sorting (only works for 100x100 map or less
def myCmp(obj):
    assert(obj)
    location = obj['location']
    return location['x']*100 + location['y']

# PURPOSE: Search lists of objects for items on the
#   same location but owned by different owners.
#   "none/nil" should count as a different owner
# RETURNS: An array of Lists of all those conflicted ownership locations
# Example:
#   conflicts[0] = Ship1, Ship2, StarBase3
#   conflicts[1] = Ship4, StarBase5
def getConflictList(objects):
    assert(objects)
    starList     = objects['starList']
    thingList    = objects['thingList']
    shipList     = objects['shipList']
    starBaseList = objects['starBaseList']
    assert(starList and thingList and shipList and starBaseList)

    allList = starList + thingList + shipList + starBaseList
    sortedList = sorted(allList, key=myCmp)
    if (sortedList):
        last = sortedList[0]
    conflicts = []
    listOfLists = []
    for obj in sortedList:
        if last['location'] == obj['location']:
            if (conflicts):
                # There is already a conflict here. That means everyone
                # is in conflict
                conflicts.append(obj)
                continue
            if last['owner'] != obj['owner']:
                print("conflict")
                # what about "last"?
                conflicts.append(last)
                conflicts.append(obj)
        else:
            if (conflicts):
                listOfLists.append(conflicts)
                conflicts = []
        last = obj
    return listOfLists

# PURPOSE: turn a conflict  into a list of ships on each side
# RETURNS: A dict of ships on each side
# Example:
#   {
#       "alex" : [alexShip1]
#       "Rex"  : [RexShip1, rexShip2]
#       "bob"  : [bobShip1, bobShip2]
#   }
def organizeConflict(conflict):
    conflictDict = {}
    for thing in conflict:
        print ("here is the thing!")
        print (thing)
        print ("the things type:")
        print (thing['type'])
        if thing['type'] == 'ship':
            if thing['owner'] not in conflictDict.keys():
                conflictDict[thing['owner']] = []
            conflictDict[thing['owner']].append(thing)
    return conflictDict

# PURPOSE: create and return an empty game
#    FIXME TODO
#    I don't think this actually insantiates a new object.
# RETURNS: new empty game
def emptyGame():
    sampleGame = {
        'options': {
            'serverIp'  : "192.168.1.5",
            'mapSize'   : {'width':10, 'height':10},
        },
        'state': {
            'turnNumber': 0,
            'phase': "nil",
            'activePlayer': "nil",
        },
        'orders': [
        ],
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
                 'BP': {'perturn':3, 'cur':20},
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
                 'BP': {'perturn':0, 'cur':15},
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
                 'BP': {'perturn':0, 'cur':10},
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
