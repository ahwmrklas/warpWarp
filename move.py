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

class menuMover:
    def __init__(self, private, x, y, shipMove):

        # This only happened when server got corrupted
        # but it was really annoying
        if (shipMove < 0):
            print("Error: move < zero:", shipMove)
            shipMove = 0

        self.private = private
        self.hexGrid = private[2]
        self.startX = x
        self.startY = y

        self.movement = shipMove

    def __call__(self):
        self.hexGrid.setLeftPrivateCallBack(moveOnClick, self.private)
        startI, startJ, startK = XYtoIJK(self.startX, self.startY)
        for i in range(-self.movement, self.movement + 1):
            for j in range(-self.movement, self.movement + 1):
                for k in range(-self.movement, self.movement + 1):
                    if i+j+k==0:
                        x,y = IJKtoXY(startI + i, startJ + j, startK + k)
                        self.hexGrid.setCell(x, y,
                                            fill=None,
                                            color1='Green',
                                            color2='Green',
                                            color3='Green',
                                            color4='Green',
                                            color5='Green',
                                            color6='Green')

#set the new onclick listener
def setupMovement(hexGrid, tkRoot):
    #set the on click listener
    private = [tkRoot, "", hexGrid, hexGrid.getLeftPrivateCallBack()]

    # create a menu
    def do_popup(private, pixel_X, pixel_Y, hex_x, hex_y):
        # display the popup menu
        popup = Menu(tkRoot, tearoff=0)
        popup.add_command(label="Ships in this sector:")
        for ship in tkRoot.game['objects']['shipList']:
            if ship['location']['x'] == hex_x and ship['location']['y'] == hex_y:
                labelString = "'%s'    Moves left: %d/%d" % (ship['name'],
                                                             ship['moves']['cur'],
                                                             ship['PD']['cur'])
                private[1] = ship['name']
                moveCommand = menuMover(private,
                                        ship['location']['x'],
                                        ship['location']['y'],
                                        ship['moves']['cur'])
                popup.add_command(label=labelString, command=moveCommand)
        try:
            #disable left click
            popup.post(pixel_X, pixel_Y)
        finally:
            popup.grab_set()
            pass

    #the true means we need the root pixel location
    hexGrid.setRightPrivateCallBack(do_popup, private)

def moveOnClick(private, x, y):
    tkRoot = private[0]
    shipName = private[1]
    hexGrid = private[2]
    #write the ship where it should be.
    print("Left Click to Move")
    for ship in tkRoot.game['objects']['shipList']:
        if ship['name'] == shipName:
            #can we move there?
            moveLeft = ship['moves']['cur']
            cur_x = ship['location']['x']
            cur_y = ship['location']['y']

            si,sj,sk = XYtoIJK(x,y)
            fi,fj,fk = XYtoIJK(cur_x,cur_y)
            delta = int((abs(si-fi) + abs(sj-fj) + abs(sk-fk)) / 2)
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
                # parmanent
                if (tkRoot.hCon is not None):
                    sendJson = warpWarCmds().moveShip(shipName, x, y)
                    tkRoot.hCon.sendCmd(sendJson)
                    resp = tkRoot.hCon.waitFor(5)
                    tkRoot.game = json.loads(resp)

                updateMap(tkRoot, hexGrid, tkRoot.game)

                #replace the old call back
                hexGrid.setLeftPrivateCallBack(private[3][0], private[3][1])
                #send event
                print ("sending event!")
                tkRoot.event_generate("<<updateMenu>>", when='tail')
                print ("sent event!")
