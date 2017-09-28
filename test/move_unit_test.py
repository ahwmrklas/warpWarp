from client import comThrd
from test.testServer import ServerTestApp
import json
import sys
import time
from cmds import warpWarCmds
from dataModel import *
#most basic test of movement: we start a server. 
#we load a game. 

plid = 845733184055071504452410
shipName="foobar"

server = ServerTestApp()
hCon = comThrd("127.0.1.1", 12345)
time.sleep(1)
print("testing")
sendJson = warpWarCmds().ping(plid)
hCon.sendCmd(sendJson)
resp = hCon.waitFor(5)


loadFile = open("test/move_unit_test.wwr", 'r')
gameString = loadFile.read()
loadFile.close()
gameDict = json.loads(gameString)
print(gameDict['objects']['shipList'])
assert(gameDict['objects']['shipList'][0]['location']['x'] == 2 and gameDict['objects']['shipList'][0]['location']['y'] == 12)

#send the game to the server.
sendJson = warpWarCmds().restoreGame(plid, gameDict)
hCon.sendCmd(sendJson)
resp = hCon.waitFor(5)
print("Game loaded")
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


sendJson = warpWarCmds().moveShip(plid, shipName, 5, 14)
hCon.sendCmd(sendJson)
resp = hCon.waitFor(5)
game = json.loads(resp)
print (game['objects']['shipList'])
assert(game['objects']['shipList'][0]['location']['x'] == 5 and game['objects']['shipList'][0]['location']['y'] == 14)
server.quit()
hCon.quitCmd()
sys.exit()
