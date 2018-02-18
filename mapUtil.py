from hexgrid import *
from tkinter import *
from hexinfo import *
import dataModel


class hexMap(HexagonalGrid):
    class HighlightSettings():
        def __init__(self,x,y,color1,color2,color3,color4,color5,color6,boldness):
            self.x = x
            self.y = y
            self.color1 = color1
            self.color2 = color2
            self.color3 = color3
            self.color4 = color4
            self.color5 = color5
            self.color6 = color6
            self.boldness = boldness

    def __init__(self, frame, tkRoot, width, height):
        self.hiliteList = []
        self.anchorFrame = frame
        self.callbackData = tkRoot

        self.__initMap(width, height)

    # PURPOSE:
    # RETURNS: hexMap handle
    def __initMap(self, width, height):

        # create a hex map that is the basis of our game display
        HexagonalGrid.__init__(self, master = self.anchorFrame, scale = 20,
                               grid_width=width,
                               grid_height=height, highlightthickness=0)

        self.setLeftPrivateCallBack(self.clickHex, self.callbackData)

    # PURPOSE: Add a highlight color to given location
    # A color of "None" erases any hilite for that location
    # RETURN: none
    def hiliteMap(self, x, y, color, boldness=2, callback=None):
        setting = self.HighlightSettings(x,y,color,color,color,color,color,color,boldness=2)
        self.hiliteList.append(setting)

    def specialHiliteMap(self, x, y, color1,color2,color3,color4,color5,color6, boldness=2, callback=None):
        setting = self.HighlightSettings(x,y,color1,color2,color3,color4,color5,color6,boldness)
        self.hiliteList.append(setting)

    # PURPOSE: Erase all hiliting
    # RETURN: none
    def unHiliteMap(self):
        self.hiliteList = []

    # PURPOSE:
    # RETURN: none
    def updateMap(self, game):
    
        print("GUI: updateMap")
        if (game is None):
            return

        # Basic grid is at bottom
        self.drawGrid('white')
    
        # Draw the warp lines
        for line in game['objects']['warpLineList']:
            base1 = dataModel.findBase(game, line['start'])
            base2 = dataModel.findBase(game, line['end'])
            if (base1 and base2):
                self.drawLine(base1['location']['x'], base1['location']['y'],
                                base2['location']['x'], base2['location']['y'])
    
        # Draw All the unique objects (plants, ships)
        allList = (game['objects']['starList'] +
                   game['objects']['thingList'] +
                   game['objects']['shipList'] +
                   game['objects']['starBaseList'])

        # Convert object list to something hexgrid can handle
        listForHexGrid = []
        for obj in allList:
            x = obj['location']['x']
            y = obj['location']['y']
            listForHexGrid.append((x,y,obj['image']))
    
        self.drawObjects(listForHexGrid)
    
        # Draw a pretty colored hilight around all the special hexes
        for hilite in self.hiliteList:
            self.setCell(hilite.x, hilite.y,
                                fill=None,
                                color1=hilite.color1,
                                color2=hilite.color2,
                                color3=hilite.color3,
                                color4=hilite.color4,
                                color5=hilite.color5,
                                color6=hilite.color6,
                                width=hilite.boldness,
                                tags=None)
    
    # PURPOSE:
    # RETURNS: Nothing ... but a return might be useful
    def clickHex(self, tkRoot, x, y):
        print("GUI: Clicked on ", x, y, " Display info about hex")

        assert(tkRoot)
        if (tkRoot.game is None):
            return

        # Find all of the things located at x,y
        xyList = []
        xyList.extend(dataModel.findObjectsAt(tkRoot.game, x, y))

        hexInfo(self.anchorFrame, tkRoot.game, xyList)
