from client import comThrd
from test.testServer import ServerTestApp
import json
import time
from cmds import warpWarCmds
from dataModel import *
#most basic test of movement: we start a server. 
#we load a game. 
ServerTestApp()
hCon = comThrd("127.0.1.1", 12345)
time.sleep(1)
print("testing")
sendJson = warpWarCmds().ping(0)
hCon.sendCmd(sendJson)
resp = hCon.waitFor(5)
print(resp)
"""
playerMe = playerTableGet(game, self.plid)
if (playerMe is None):
    playerMe = {'phase':None}

# What is the current game state and player state?
if ( (gamePhase == game['state']['phase']) and
     (playerPhase == playerMe['phase']) ):
     continue

gamePhase   = game['state']['phase']
playerPhase = playerMe['phase']
#we move a ship. 
{'plid': 845733184055071504452410, 'cmd': 'moveship', 'y': 14, 'name': 'foobar', 'x': 5}
#we verify that the ship has moved
"""
