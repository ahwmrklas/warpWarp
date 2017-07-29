from hexgrid import *
from tkinter import *
from overlay import *
from hexinfo import *
import dataModel


class hexMap(HexagonalGrid):
    def __init__(self, tkRoot, width, height):
        self.hiliteList = []
        self.anchorFrame = tkRoot.mapFrame
        self.callbackData = tkRoot

        self.initMap(width, height)

    # PURPOSE:
    # RETURNS: hexMap handle
    def initMap(self, width, height):

        # create a hex map that is the basis of our game display
        HexagonalGrid.__init__(self, master = self.anchorFrame, scale = 20,
                               grid_width=width,
                               grid_height=height)

        self.setLeftPrivateCallBack(self.clickHex, self.callbackData)

        # Locate the hexmap on the tkinter "grid"
        self.grid(row=0, column=0, padx=10, pady=10)

    # PURPOSE: Add a highlight color to given location
    # A color of "None" erases any hilite for that location
    # RETURN: none
    def hiliteMap(self, x, y, color, callback):
        print("HLMap", x,y,color)
        self.hiliteList.append((x,y,color,callback))

    # PURPOSE: Erase all hiliting
    # RETURN: none
    def unHiliteMap(self):
        self.hiliteList = []

    # PURPOSE: 
    # RETURN: none
    def resizeMap(self, width, height):
        # don't resize if it is already the same size?
        #if ((width != self.grid_width) or
        #    (height != self.grid_height)):
        self.initMap(width, height)
        self.unHiliteMap()

    # PURPOSE:
    # RETURN: none
    def updateMap(self, game):
    
        if (game is None):
            return
    
        if ((game['map']['width'] != self.grid_width) or
            (game['map']['height'] != self.grid_height)):
            self.resizeMap(game['map']['width'], game['map']['height'])
    
        self.drawGrid('white')
    
        # Draw a pretty colored hilight around all the special hexes
        for hilite in self.hiliteList:
            print("hilight", hilite)
            self.setBorders(hilite[0], hilite[1], hilite[2])
    
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
    
        self.drawObjects(objArray)
    
        for line in warpLineList:
            base1 = dataModel.findBase(game, line['start'])
            base2 = dataModel.findBase(game, line['end'])
            if (base1 and base2):
                self.drawLine(base1['location']['x'], base1['location']['y'],
                                base2['location']['x'], base2['location']['y'])

    # PURPOSE:
    # RETURNS: Nothing ... but a return might be useful
    def clickHex(self, tkRoot, x, y):
        print("Clicked on ", x, y, " Display info about hex")

        # Find all of the things located at x,y
        lists = tkRoot.game['objects']
        starList = lists['starList']
        starBaseList = lists['starBaseList']
        thingList = lists['thingList']
        shipList = lists['shipList']
        xyList = []
        xyList.extend(dataModel.findObjectsAt(starList, x, y))
        xyList.extend(dataModel.findObjectsAt(thingList, x, y))
        xyList.extend(dataModel.findObjectsAt(shipList, x, y))
        xyList.extend(dataModel.findObjectsAt(starBaseList, x, y))

        hexInfo(tkRoot.mapFrame, xyList)
