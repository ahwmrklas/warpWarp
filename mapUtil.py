from hexgrid import *
from tkinter import *
from overlay import *
from hexinfo import *
import dataModel

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
def initMap(tkRoot, width, height):

    # create a hex map that is the basis of our game display
    hexMap = HexagonalGrid(tkRoot.mapFrame, scale = 20, grid_width=width,
                           grid_height=height)

    hexMap.setLeftPrivateCallBack(clickHex, tkRoot)

    # Locate the hexmap on the tkinter "grid"
    hexMap.grid(row=0, column=0, padx=10, pady=10)

    # display the whole hexMap.
    hexMap.drawGrid('white')

    return hexMap

# PURPOSE:
# RETURN: none
def updateMap(tkRoot, game):

    if (game is None):
        return

    if ((game['map']['width'] != tkRoot.hexMap.grid_width) or
        (game['map']['height'] != tkRoot.hexMap.grid_height)):
        tkRoot.hexMap = initMap(tkRoot, game['map']['width'], game['map']['height'])

    tkRoot.hexMap.drawGrid('white')

    #super annoying bit of complexity here. if we are in combat, we need to 
    #draw red borders around all combat hexes. We will have to find the
    #combat list again, even though we already found it in update phase menu.
    if tkRoot.game['state']['phase'] == 'combat':
        conflictList = dataModel.getConflictList(tkRoot.game['objects'])
        for conflict in conflictList:
            tkRoot.hexMap.setBorders(int(conflict[0]['location']['x']),
                    int(conflict[0]['location']['y']), 'Red')

    dim = game['map']
    lists = game['objects']
    starList = lists['starList']
    thingList = lists['thingList']
    shipList = lists['shipList']
    starBaseList = lists['starBaseList']
    warpLineList = lists['warpLineList']

    # Break up the objectlists into a 2D array. I don't like this
    # but for the moment it works
    objArray = DrawArray(dim['width'], dim['height'], game['objects'])

    tkRoot.hexMap.drawObjects(objArray)

    for line in warpLineList:
        base1 = dataModel.findBase(tkRoot.game, line['start'])
        base2 = dataModel.findBase(tkRoot.game, line['end'])
        if (base1 and base2):
            tkRoot.hexMap.drawLine(base1['location']['x'], base1['location']['y'],
                            base2['location']['x'], base2['location']['y'])

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

    hexInfo(tkRoot.mapFrame, xyList)
