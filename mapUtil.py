from hexgrid import *
from tkinter import *
from hexinfo import *
import dataModel


class hexMap(HexagonalGrid):
    def __init__(self, tkRoot, width, height):
        self.hiliteList = []
        self.anchorFrame = tkRoot.mapFrame
        self.callbackData = tkRoot

        self.__initMap(width, height)
        self.pack(fill=BOTH, expand=YES)

    # PURPOSE:
    # RETURNS: hexMap handle
    def __initMap(self, width, height):

        # create a hex map that is the basis of our game display
        HexagonalGrid.__init__(self, master = self.anchorFrame, scale = 20,
                               grid_width=width,
                               grid_height=height, highlightthickness=0)

        self.setLeftPrivateCallBack(self.clickHex, self.callbackData)

        # Locate the hexmap on the tkinter "grid"
        self.grid(row=0, column=0, padx=10, pady=10)

    # PURPOSE: Add a highlight color to given location
    # A color of "None" erases any hilite for that location
    # RETURN: none
    def hiliteMap(self, x, y, color, boldness=2, callback=None):
        self.hiliteList.append((x,y,color,boldness,callback))

    # PURPOSE: Erase all hiliting
    # RETURN: none
    def unHiliteMap(self):
        self.hiliteList = []

    # PURPOSE: Only resize if needed
    # RETURN: none
    def resizeMap(self, width, height):
        # don't resize if it is already the same size?
        if ((width != self.grid_width) or (height != self.grid_height)):
            self.__initMap(width, height)
            self.pack(fill=BOTH, expand=YES)
            self.unHiliteMap()

    # PURPOSE:
    # RETURN: none
    def updateMap(self, game):
    
        print("updateMap")
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
            self.setBorders(hilite[0], hilite[1], hilite[2], hilite[3])

        for hist in game['history']:
            print(hist)
        print("five")
    
    # PURPOSE:
    # RETURNS: Nothing ... but a return might be useful
    def clickHex(self, tkRoot, x, y):
        print("Clicked on ", x, y, " Display info about hex")

        assert(tkRoot)
        if (tkRoot.game is None):
            return

        # Find all of the things located at x,y
        xyList = []
        xyList.extend(dataModel.findObjectsAt(tkRoot.game, x, y))

        hexInfo(tkRoot.mapFrame, xyList)
