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

# PURPOSE: look up base name in game base & star list
#   (Stars and Bases are mostly interchangeable. They should be in one list)
# RETURNS: entry of base
def findBase(game, baseName):
    for base in game['objects']['starBaseList']:
        if base['name'] == baseName:
            return base
    for base in game['objects']['starList']:
        if base['name'] == baseName:
            return base
    # FIXME ... should we really look in thinglist?
    # I imagined "things" couldn't be used to build ships ...
    # BUt they might have build points on them.
    for thing in game['objects']['thingList']:
        if thing['name'] == baseName:
            return thing
    return None

# PURPOSE:
# RETURNS: list of objects at given location
def findObjectsAt(game, x, y):
    if (game is None):
        return []
    assert(game) # I want an assert here ... but sometimes game was "None"

    objects = game['objects']
    assert(objects)

    starList     = objects['starList']
    thingList    = objects['thingList']
    shipList     = objects['shipList']
    starBaseList = objects['starBaseList']

    allList = starList + thingList + shipList + starBaseList
    atLocation = []
    for obj in allList:
        if ( x == obj['location']['x'] and y == obj['location']['y']):
            atLocation.append(obj)

    return atLocation

#If x,y is a hex with a warpline, return a list of x and ys for the other ends
def getWarpLineEnd(game, x,y):

    #if they go to one of these locations, it only costs one
    warpEnds = []
    for line in game['objects']['warpLineList']:
        base1 = findBase(game, line['start'])
        base2 = findBase(game, line['end'])
        assert(base1 and base2)
        if (base1['location']['x'] == x and base1['location']['y'] == y):
            warpEnds.append( [base2['location']['x'], base2['location']['y'] ])
        if (base2['location']['x'] == x and base2['location']['y'] == y):
            warpEnds.append( [base1['location']['x'], base1['location']['y'] ])

    return warpEnds

# PURPOSE: Return the player structure from the game
# RETURNS: player table
def playerTableGet(game, playerName):
    if (not game):
        return None

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
#   "None" should count as a different owner
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
    nonShipList = []
    for thing in conflict:
        print ("here is the thing!")
        print (thing)
        print ("the things type:")
        print (thing['type'])
        if thing['type'] == 'ship':
            if thing['owner'] not in conflictDict.keys():
                conflictDict[thing['owner']] = []
            conflictDict[thing['owner']].append(thing)
        else:
            nonShipList.append(thing)

    return conflictDict, nonShipList

# PURPOSE: These are combat orders ... which really isn't the game
#          representation. But I wanted this in more than one module
# RETURNS: string representation of given order
def prettyOrders(order):
    if not order:
        return ""

    tactic = order['tactic'][0]
    drive  = order['tactic'][1]
    beamTarget  = order['beams'][0]
    beamPower   = order['beams'][1]
    screenPower = order['screens']
    pretty = "%s: D=%d, B=(%d, %s), S=%d" % (tactic, drive, beamPower, beamTarget, screenPower)
    missiles = ""
    for missile in order['missiles']:
        missiles += "\nT=(%d, %s)" % (missile[1], missile[0])

    return pretty + missiles

# PURPOSE: create and return an empty game
#    This should be displayed when players first connect
#    We could make this some fancy graphic ... if we wanted to work it out
# RETURNS: new empty game
def emptyGame():
    empty = {
        'options': {
        },
        'state': {
            'turnNumber': 0,
            'phase': None,
            'activePlayer': None,
        },
        'orders': {
        },
        'map': {'width':10, 'height':10},
        'playerList': [
        ],
        'objects': {
            'starList': [
            ],
            'thingList': [
            ],
            'shipList': [
            ],
            'starBaseList': [
            ],
            'warpLineList': [
            ],
        },
        'history': [
        ],
    }
    return empty

# PURPOSE: create and return the default WarpWar map
#    This is the game to start playing
#    FIXME TODO
#    I don't think this actually insantiates a new object.
# RETURNS: new default WarpWar map
def defaultGame():
    defaultGame = {
        'options': {
            'serverIp'  : "192.168.1.5",
            'mapSize'   : {'width':21, 'height':15},
        },
        'state': {
            'turnNumber': 0,
            'phase': None,
            'activePlayer': None,
        },
        'orders': {
        },
        'map': {'width':21, 'height':15},
        'playerList': [
        ],
        'objects': {
            'starList': [
                {'name':"Mosul",
                 'type': "star",
                 'location': {'x':1, 'y':4},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Ur",
                 'type': "star",
                 'location': {'x':2, 'y':8},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Larsu",
                 'type': "star",
                 'location': {'x':2, 'y':12},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Sippur",
                 'type': "star",
                 'location': {'x':4, 'y':3},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Erech",
                 'type': "star",
                 'location': {'x':4, 'y':5},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Calah",
                 'type': "star",
                 'location': {'x':4, 'y':9},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Susa",
                 'type': "star",
                 'location': {'x':5, 'y':14},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Byblos",
                 'type': "star",
                 'location': {'x':6, 'y':3},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Adab",
                 'type': "star",
                 'location': {'x':6, 'y':7},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Nippur",
                 'type': "star",
                 'location': {'x':7, 'y':11},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Ubaid",
                 'type': "star",
                 'location': {'x':8, 'y':4},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Khaha",
                 'type': "star",
                 'location': {'x':8, 'y':9},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Assur",
                 'type': "star",
                 'location': {'x':10, 'y':13},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Mari",
                 'type': "star",
                 'location': {'x':10, 'y':7},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Lagash",
                 'type': "star",
                 'location': {'x':11, 'y':10},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Elam",
                 'type': "star",
                 'location': {'x':12, 'y':8},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Sumarra",
                 'type': "star",
                 'location': {'x':13, 'y':2},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Umma",
                 'type': "star",
                 'location': {'x':14, 'y':6},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Girsu",
                 'type': "star",
                 'location': {'x':13, 'y':9},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Jarmo",
                 'type': "star",
                 'location': {'x':12, 'y':12},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Isin",
                 'type': "star",
                 'location': {'x':15, 'y':2},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Sumer",
                 'type': "star",
                 'location': {'x':16, 'y':5},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Akkad",
                 'type': "star",
                 'location': {'x':16, 'y':8},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Kish",
                 'type': "star",
                 'location': {'x':15, 'y':11},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Eridu",
                 'type': "star",
                 'location': {'x':16, 'y':13},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Nineveh",
                 'type': "star",
                 'location': {'x':19, 'y':4},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Babylon",
                 'type': "star",
                 'location': {'x':18, 'y':7},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
                {'name':"Ugarit",
                 'type': "star",
                 'location': {'x':20, 'y':12},
                 'image':"alpha.png",
                 'owner':None,
                 'BP': {'perturn':3, 'cur':20},
                },
            ],
            'thingList': [
                {'name':"AncientRelic",
                 'type': "special",
                 'location': {'x':4, 'y':7},
                 'image':"relic.png",
                 'owner':None,
                 'BP': {'perturn':0, 'cur':15},
                 'visibility':[],
                },
            ],
            'shipList': [
            ],
            'starBaseList': [
                {'name': "Babylon_4",
                 'type': "base",
                 'location': {'x':8, 'y':4},
                 'image': "b_5.png",
                 'owner': None,
                 'BP': {'perturn':0, 'cur':10},
                },
                {'name': "Babylon_5",
                 'type': "base",
                 'location': {'x':4, 'y':8},
                 'image': "b_5.png",
                 'owner': None,
                 'BP': {'perturn':0, 'cur':10},
                },
            ],
            'warpLineList': [
                {'start': "Mosul", 'end': "Sippur"},
                {'start': "Erech",  'end': "Adab"},
                {'start': "Larsu",  'end': "Susa"},
                {'start': "Calah",  'end': "Nippur"},
                {'start': "Byblos",  'end': "Adab"},
                {'start': "Adab",  'end': "Khaha"},
                {'start': "Nippur",  'end': "Lagash"},
                {'start': "Nippur",  'end': "Assur"},
                {'start': "Lagash",  'end': "Assur"},
                {'start': "Lagash",  'end': "Elam"},
                {'start': "Ubaid",  'end': "Mari"},
                {'start': "Ubaid",  'end': "Sumarra"},
                {'start': "Umma",  'end': "Sumarra"},
                {'start': "Umma",  'end': "Mari"},
                {'start': "Umma",  'end': "Girsu"},
                {'start': "Umma",  'end': "Sumer"},
                {'start': "Babylon",  'end': "Sumer"},
                {'start': "Isin",  'end': "Nineveh"},
                {'start': "Ugarit",  'end': "Eridu"},
                {'start': "Kish",  'end': "Eridu"},
                {'start': "Kish",  'end': "Akkad"},
                {'start': "Kish",  'end': "Jarmo"},
                {'start': "Ur",  'end': "Erech"},
            ],
        },
        'history': [
        ],
    }
    return defaultGame
