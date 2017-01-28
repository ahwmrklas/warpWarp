# Sample dictionary data game

from enum import Enum

class eCmd(Enum):
    eStart = 1
    eBuild = 2

class ePhase(Enum):
    eNil             = 1
    eCreating        = 2
    eBuild           = 3
    eMovement        = 4
    eCombat          = 5
    eBattle          = 6
    eDamageSelection = 7
    eWinnerBoard     = 8

# Sample dictionary data game
sampleGame = {
    'options': {
        'serverIp'  : "192.168.1.5",
        'mapSize'   : {'width':10, 'height':10},
        'startingBP': 20,
        'perTurnBP' :  5,
    },
    'state': {
        'turnNumber': 0,
        'phase': "creating",
        'activePlayer': "dad",
    },
    'map': {'width':10, 'height':10},
    'playerList': [
        {'name': "dad"},
        {'name': "Alex"},
    ],
    'objects': {
        'starList': [
            {'name':"Alpha",
             'type': "star",
             'location': {'x':1, 'y':3},
             'image':"alpha.png",
             'owner':"dad",
             'valueBP':3,
             'visibility':[ {'player':"dad",  'percent':100},
                            {'player':"alex", 'percent':30},
                          ],
            },
        ],
        'thingList': [
            {'name':"AncientRelic",
             'type': "special",
             'location': {'x':4, 'y':7},
             'image':"relic.png",
             'owner':"none",
             'valueBP':0,
             'visibility':[ {'player':"dad",  'percent':100},
                            {'player':"alex", 'percent':30},
                          ],
            },
        ],
        'shipList': [
            {'name': "first",
             'type': "ship",
             'location': {'x':4, 'y':3},
             'image':"warpship.png",
             'owner':"dad",
             'techLevel': 1,
             'moves': {'cur':3},   # relates to PowerDrive
             'PD':{'max':5, 'cur':5},       # PowerDrive
             'WG':{'max':True, 'cur':True}, # Warp Generator
             'B': {'max':3, 'cur':3},       # Beams
             'S': {'max':2, 'cur':2},       # Screens (Shields)
             'E': {'max':2, 'cur':2},       # Electronic Counter Measures (New)
             'T': {'max':3, 'cur':3},       # Tubes
             'M': {'max':7, 'cur':7},       # Missiles
             'A': {'max':2, 'cur':2},       # Armor (New)
             'C': {'max':1, 'cur':1},       # Cannons (New)
             'SH':{'max':2, 'cur':2},       # Shells (New)
             'SR':{'max':3, 'cur':3},       # System Ship Racks
             'H': {'max':1, 'cur':1},       # Holds (New)
             'R': {'max':1, 'cur':1},       # Repair Bays (New)
             'visibility':[ {'player':"dad",  'percent':100},
                            {'player':"alex", 'percent':30},
                          ],
            },
        ],
        'starBaseList': [
            {'name': "Babylon 5",
             'type': "base",
             'location': {'x':4, 'y':8},
             'image': "b_5.png",
             'owner': "Alex",
             'stockpile': 15,
            },
        ],
        'warpLineList': [
            {'start': "Alpha", 'end': "Beta"},
            {'start': "Beta",  'end': "Alpha"},
        ],
    },
    'history': [
        {'cmd':"start", 'player':"dad"},
        {'cmd':"build", 'player':"dad"},
    ],
}
