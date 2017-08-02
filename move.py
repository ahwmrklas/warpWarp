"""
Purpose: move the selected ship. 
"""


from hexgrid import *
from tkinter import *
from xbm import TileContent
from dataModel import *
from mapUtil import *
from ijk import *
from cmds import warpWarCmds
import json

# PURPOSE:
# RETURNS:
def createMoveGraph(tkRoot, game, hexMap, shipName):
    ship = findShip(game, shipName)
    startI, startJ, startK = XYtoIJK(ship['location']['x'], ship['location']['y'])
    movesLeft = ship['moves']['cur']
    for i in range(-movesLeft, movesLeft + 1):
        for j in range(-movesLeft, movesLeft + 1):
            for k in range(-movesLeft, movesLeft + 1):
                if i+j+k==0:
                    x,y = IJKtoXY(startI + i, startJ + j, startK + k)
                    hexMap.setBorders(x, y, 'Green')

    #if they go to one of these locations, it only costs one
    warpEnds = getWarpLineEnd(game, ship['location']['x'], ship['location']['y'])
    for warpEnd in warpEnds:
            hexMap.setBorders(warpEnd[0], warpEnd[1], 'Yellow')
    private = [tkRoot, shipName, tkRoot.hexMap.getLeftPrivateCallBack(), warpEnds]
    hexMap.setLeftPrivateCallBack(moveOnClick, private)

#set the new onclick listener
def setupRightClickMoveMenu(hexMap, tkRoot):

    # create a menu
    def do_popup(private, pixel_X, pixel_Y, hex_x, hex_y):
        # display the popup menu
        popup = Menu(tkRoot, tearoff=0)
        popup.add_command(label="Ships in this sector:")
        for ship in tkRoot.game['objects']['shipList']:
            if ship['location']['x'] == hex_x and ship['location']['y'] == hex_y:
                if (ship['owner'] == tkRoot.playerName):
                    if (ship['WG']['cur'] == True):
                        labelString = "'%s'    Moves left: %d/%d" % (ship['name'],
                                                                     ship['moves']['cur'],
                                                                     ship['PD']['cur'])
                        popup.add_command(label=labelString,
                                  command=lambda game=tkRoot.game,
                                                 hexMap=tkRoot.hexMap,
                                                 shipName=ship['name']:
                                                 createMoveGraph(tkRoot, game, hexMap, shipName))
        try:
            #disable left click
            popup.post(pixel_X, pixel_Y)
        finally:
            popup.grab_set()
            pass

    hexMap.setRightPrivateCallBack(do_popup, None)

def moveOnClick(private, x, y):
    tkRoot = private[0]
    shipName = private[1]
    original = private[2]
    warpEnds = private[3]
    #write the ship where it should be.
    print("Left Click to Move", shipName)
    ship = findShip(tkRoot.game, shipName)

    #can we move there?
    moveLeft = ship['moves']['cur']
    cur_x = ship['location']['x']
    cur_y = ship['location']['y']

    si,sj,sk = XYtoIJK(x,y)
    fi,fj,fk = XYtoIJK(cur_x,cur_y)
    delta = int((abs(si-fi) + abs(sj-fj) + abs(sk-fk)) / 2)
    if [x,y] in warpEnds:
        delta = 1
    if (delta <= moveLeft):
        ship['location']['x'] = x
        ship['location']['y'] = y
        #find the ijk stuff for decrementing the right number of moves
        ship['moves']['cur'] = ship['moves']['cur'] - delta

        # Send the move command to the server
        # We could also Queue up all the move commands
        # and play them out to the server later.
        # That would permit the user to change their
        # mind about a move and cancel it before it is
        # permanent
        if (tkRoot.hCon is not None):
            sendJson = warpWarCmds().moveShip(ship['owner'], shipName, x, y)
            tkRoot.hCon.sendCmd(sendJson)
            resp = tkRoot.hCon.waitFor(5)
            tkRoot.game = json.loads(resp)

        # Restore the old call back
        tkRoot.hexMap.setLeftPrivateCallBack(original[0], original[1])
        #send event
        tkRoot.event_generate("<<updateWWMenu>>", when='tail')
