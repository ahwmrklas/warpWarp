from hexgrid import *
from tkinter import *
from overlay import *
from hexinfo import *
# PURPOSE:
# RETURNS: list of objects at x,y
def findObjectsAt(objList, x, y):
    retList = []
    for obj in objList:
        if ( x == obj['location']['x'] and y == obj['location']['y']):
           retList.append(obj)
    return retList


# PURPOSE:
# RETURNS: hexMap handle
def initMap(tkRoot, game):

    dim = game['map']

    # create a hex map that is the basis of our game display
    hexMap = HexagonalGrid(tkRoot, scale = 20, grid_width=dim['width'],
                           grid_height=dim['height'])

    hexMap.setPrivateCallBack(clickHex, tkRoot)

    # Locate the hexmap on the tkinter "grid"
    hexMap.grid(row=0, column=0, padx=10, pady=10)

    # display the whole hexMap.
    hexMap.drawGrid('blue')

    return hexMap

# PURPOSE:
# RETURN: none
def updateMap(tkRoot, hexMap, game):

    hexMap.drawGrid('blue')
    dim = game['map']
    lists = game['objects']
    starList = lists['starList']
    thingList = lists['thingList']
    shipList = lists['shipList']
    starBaseList = lists['starBaseList']

    # Break up the objectlists into a 2D array. I don't like this
    # but for the moment it works
    objArray = DrawArray(dim['width'], dim['height'], game['objects'])

    hexMap.drawObjects(objArray)

# PURPOSE:
# RETURNS: Nothing ... but a return might be useful
def clickHex(tkRoot, x, y):
    print("Clicked on ", x, y, " Display info about hex")

    # Find all of the things located at x,y
    lists = tkRoot.game['objects']
    starList = lists['starList']
    starBaseList = lists['starBaseList']
    thingList = lists['thingList']
    shipList = lists['shipList']
    xyList = []
    xyList.extend(findObjectsAt(starList, x, y))
    xyList.extend(findObjectsAt(thingList, x, y))
    xyList.extend(findObjectsAt(shipList, x, y))
    xyList.extend(findObjectsAt(starBaseList, x, y))

    hexInfo(tkRoot, xyList)

