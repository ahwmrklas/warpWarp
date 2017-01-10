"""
Purpose: move the selected ship. 
"""


from hexgrid import *
from tkinter import *
from xbm import TileContent
from dataModel import *
from mapUtil import *

#set the new onclick listener
def hexMove(hexGrid, tkRoot, shipName):
    #set the on click listener
    private = [tkRoot, shipName, hexGrid]
    hexGrid.setPrivateCallBack(moveOnClick, private)

def moveOnClick(private, x, y):
    tkRoot = private[0]
    shipName = private[1]
    hexGrid = private[2]
    #write the ship where it should be.
    for ship in tkRoot.game['objects']['shipList']:
        if ship['name'] == shipName:
            ship['location']['x'] = x
            ship['location']['y'] = y
            updateMap(tkRoot, hexGrid, tkRoot.game)
