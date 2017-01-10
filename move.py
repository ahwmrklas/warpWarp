"""
Purpose: move the selected ship. 
"""


from hexgrid import *
from tkinter import *
from xbm import TileContent
from dataModel import *
from mapUtil import *

class menuMover:
    def __init__(self, private, x, y, shipMove):
        self.private = private
        self.hexGrid = private[2]
        self.startX = x
        self.startY = y
        self.movement = shipMove
    def __call__(self):
        print (self.startX)
        print (self.startY)
        print (self.movement)
        self.hexGrid.setPrivateCallBack(moveOnClick, self.private)

#set the new onclick listener
def setupMovement(hexGrid, tkRoot):
    #set the on click listener
    private = [tkRoot,"", hexGrid, hexGrid.getPrivateCallBack()]

    # create a menu
    def do_popup(private, root_x, root_y, hex_x, hex_y):
        # display the popup menu
        print (root_x)
        print (root_y)
        popup = Menu(tkRoot, tearoff=0)
        popup.add_command(label="Ships in this sector:")
        for ship in tkRoot.game['objects']['shipList']:
            if ship['location']['x'] == hex_x and ship['location']['y'] == hex_y:
                labelString = "'%s'    Moves left: %d/%d" % (ship['name'], ship['PD']['cur'], ship['PD']['max'])
                private[1] = ship['name']
                moveCommand = menuMover(private, ship['location']['x'], ship['location']['y'], ship['PD']['cur'])
                popup.add_command(label=labelString, command=moveCommand)
        try:
            #disable left click
            popup.post(root_x, root_y)
        finally:
            popup.grab_set()
            pass

    hexGrid.setRightPrivateCallBack(do_popup, private, True) #the true means we need the root pixel location

def moveOnClick(private, x, y):
    tkRoot = private[0]
    shipName = private[1]
    hexGrid = private[2]
    #write the ship where it should be.
    for ship in tkRoot.game['objects']['shipList']:
        if ship['name'] == shipName:
            #can we move there?
            moveLeft = ship['PD']['cur']
            cur_x = ship['location']['x']
            cur_y = ship['location']['y']

            if (abs(x - cur_x) + abs(y - cur_y) <= moveLeft):
                ship['location']['x'] = x
                ship['location']['y'] = y
                ship['PD']['cur'] = ship['PD']['cur'] - (abs(x - cur_x) + abs(y - cur_y))

                updateMap(tkRoot, hexGrid, tkRoot.game)

                #replace the old call back
                hexGrid.setPrivateCallBack(private[3][0], private[3][1])
