# Sample dictionary data game

from enum import Enum

class eCmd(Enum):
    eStart = 1
    eBuild = 2

class ePhase(Enum):
    eNil             = 1 # Can only create game (or ping)
    eCreating        = 2 # join game, Say ready/done, Start game (or quit, ping)
    eBuild           = 3 # build ship, Say ready/done
    eMovement        = 4 # Move, Say ready
    eCombat          = 5 # ? select a first battle?
    eBattle          = 6 # Provide ship orders
    eDamageSelection = 7 # Provide damage allocation
    eWinnerBoard     = 8 # Nothing? Look at results? Add name to high scores?

# Sample dictionary data game
sampleGame = {
    'options': {
        'serverIp'  : "192.168.1.5",
        'mapSize'   : {'width':10, 'height':10},
        #'startingBP': 20,
        #'perTurnBP' :  5,
    },
    'state': {
        'turnNumber': 0,
        'phase': "nil",
        'activePlayer': "ahw",
    },
    'orders': {
    },
    'map': {'width':10, 'height':10},
    'playerList': [
        {'name': "ahw",  'phase': "nil"},
        {'name': "bearda", 'phase': "nil"},
    ],
    'objects': {
        'starList': [
            {'name':"Alpha",
             'type': "star",
             'location': {'x':1, 'y':3},
             'image':"alpha.png",
             'owner':"ahw",
             'BP': {'perturn':3, 'cur':20},
             'visibility':[ {'player':"ahw",  'percent':100},
                            {'player':"bearda", 'percent':30},
                          ],
            },
            {'name':"Beta",
             'type': "star",
             'location': {'x':6, 'y':3},
             'image':"alpha.png",
             'owner':"ahw",
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
             'owner':"none",
             'BP':{'perturn':0, 'cur':10},
             'visibility':[ {'player':"ahw",  'percent':100},
                            {'player':"bearda", 'percent':30},
                          ],
            },
        ],
        'shipList': [
            {'name': "first",
             'type': "ship",
             'location': {'x':4, 'y':3},
             'image':"warpship.png",
             'owner':"ahw",
             'techLevel': 1,
             'damage': 0,
             'moves': {'cur':3},   # relates to PowerDrive
             'PD':{'max':5, 'cur':5},       # PowerDrive
             'WG':{'max':True, 'cur':True}, # Warp Generator
             'B': {'max':3, 'cur':3},       # Beams
             'S': {'max':2, 'cur':2},       # Screens (Shields)
             'E': {'max':0, 'cur':0},       # Electronic Counter Measures (New)
             'T': {'max':3, 'cur':3},       # Tubes
             'M': {'max':7, 'cur':7},       # Missiles
             'A': {'max':2, 'cur':2},       # Armor (New)
             'C': {'max':1, 'cur':1},       # Cannons (New)
             'SH':{'max':2, 'cur':2},       # Shells (New)
             'SR':{'max':3, 'cur':3},       # System Ship Racks
             'H': {'max':1, 'cur':1},       # Holds (New)
             'R': {'max':1, 'cur':1},       # Repair Bays (New)
             'visibility':[ {'player':"ahw",  'percent':100},
                            {'player':"bearda", 'percent':30},
                          ],
            },
        ],
        'starBaseList': [
            {'name': "Babylon 5",
             'type': "base",
             'location': {'x':4, 'y':8},
             'image': "b_5.png",
             'owner': "bearda",
             'BP':{'perturn':0, 'cur':10},
            },
        ],
        'warpLineList': [
            {'start': "Alpha", 'end': "Beta"},
            {'start': "Beta",  'end': "Alpha"},
        ],
    },
    'history': [
        {'cmd':"start", 'player':"ahw"},
        {'cmd':"build", 'player':"ahw"},
    ],
}
