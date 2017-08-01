from tkinter import *
from xbm import TileContent
from xbm import TileFiles

# HexaCanvas inherits from Canvas
class HexaCanvas(Canvas):
    """ A canvas that provides a create-hexagone method """
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.hexaSize = 20
        self.setHexaSize(self.hexaSize)

    def setHexaSize(self, number):
        self.hexaSize = number
        self.Δx = (self.hexaSize**2 - (self.hexaSize/2)**2)**0.5


    def create_hexagone(self, x, y, content = TileContent.NO_ITEMS,
            color = "black", fill="blue",
            color1=None, color2=None, color3=None, color4=None, color5=None,
            color6=None, width=2):
        """ 
        Compute coordinates of 6 points relative to a center position.
        Point are numbered following this schema :

        Points in euclidiean grid:  
                    6

                5       1
                    .
                4       2

                    3

        Each color is applied to the side that link the vertex with same
        number to its following.
        Ex : color 1 is applied on side (vertex1, vertex2)

        Take care that tkinter ordinate axes is inverted to the standard
        euclidian ones.
        Point on the screen will be horizontally mirrored.
        Displayed points:

                    3
              color3/      \color2      
                4       2
            color4|     |color1
                5       1
              color6\      /color6
                    6

        """
        size = self.hexaSize
        Δx  = self.Δx

        point1 = (x+Δx, y+size/2)
        point2 = (x+Δx, y-size/2)
        point3 = (x   , y-size  )
        point4 = (x-Δx, y-size/2)
        point5 = (x-Δx, y+size/2)
        point6 = (x   , y+size  )

        #this setting allow to specify a different color for each side.
        if color1 == None:
            color1 = color
        if color2 == None:
            color2 = color
        if color3 == None:
            color3 = color
        if color4 == None:
            color4 = color
        if color5 == None:
            color5 = color
        if color6 == None:
            color6 = color

        self.create_line(point1, point2, fill=color1, width=width)
        self.create_line(point2, point3, fill=color2, width=width)
        self.create_line(point3, point4, fill=color3, width=width)
        self.create_line(point4, point5, fill=color4, width=width)
        self.create_line(point5, point6, fill=color5, width=width)
        self.create_line(point6, point1, fill=color6, width=width)

        #set stippling options.
        stipple = TileFiles[content]

        if fill != None:
            self.create_polygon(point1, point2, point3, point4, point5, point6,
                    fill=fill, stipple=stipple)


# HexagonalGrid inherits from HexaCanvas
class HexagonalGrid(HexaCanvas):
    # A grid whose each cell is hexagonal
    def __init__(self, master, scale, grid_width, grid_height, *args, **kwargs):

        self.grid_width  = grid_width
        self.grid_height = grid_height
        Δx     = (scale**2 - (scale/2.0)**2)**0.5
        width  = 2 * Δx * grid_width + Δx
        height = 1.5 * scale * grid_height + 0.5 * scale
        self.rightExternalCallBack = None
        self.lastX = 0
        self.lastY = 0

        HexaCanvas.__init__(self, master, background='white', width=width, height=height, *args, **kwargs)
        self.bind("<Button-1>", self.leftClickCallback)
        self.bind("<Button-3>", self.rightClickCallback)
        self.bind("<Enter>", self.Enter)
        self.bind("<Leave>", self.Leave)
        self.setHexaSize(scale)

    def setCell(self, xCell, yCell, *args, **kwargs ):
        # Create a content in the cell of coordinates x and y. Could specify
        # options throught keywords : color, fill, color1, color2, color3,
        # color4; color5, color6

        #compute pixel coordinate of the center of the cell:
        [pix_x, pix_y] = self.findPixel(xCell, yCell)

        self.create_hexagone(pix_x, pix_y, *args, **kwargs)

    # PURPOSE: Draw the entire grid with the given color
    def drawGrid(self, color):
        for x in range(0, self.grid_width):
            for y in range(0, self.grid_height):
                self.setCell(x,y, fill=color)

    #PURPOSE: read the dictionary and display it
    #RETURNS: Nothing
    def drawObjects(self, drawArray):
        self.photoList = []
        for x in range(self.grid_width):
            for y in range (self.grid_height):
                self.drawObject(x, y, drawArray.array[x][y][0])

    #PURPOSE: Draw an object on top of a hex grid
    #RETURNS: Nothing
    def drawObject(self, xCell, yCell, imageStr):
        #did we get a real image?
        if imageStr == "":
            return
        #compute pixel coordinate of the center of the cell:
        [pix_x, pix_y] = self.findPixel(xCell, yCell)
        photo = PhotoImage(file="resource/images/" + imageStr)
        self.photoList.append(
                photo.subsample(int(photo.width()/self.hexaSize)))
        self.create_image(pix_x,pix_y,image=self.photoList[-1])

    # PURPOSE: Draw line from then center of one cell to another
    # RETURNS: None
    def drawLine(self, xStart, yStart, xEnd, yEnd):
        startpix_x, startpix_y = self.findPixel(xStart, yStart)
        endpix_x,   endpix_y   = self.findPixel(xEnd,   yEnd)
        self.create_line((startpix_x, startpix_y), (endpix_x, endpix_y), fill="Yellow", width=2)

    def findPixel(self, xCell, yCell):
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5

        pix_x = Δx + 2*Δx*xCell
        if yCell%2 ==1 :
            pix_x += Δx

        pix_y = size + yCell*1.5*size
        pix_x = int(pix_x)
        pix_y = int(pix_y)
        return [pix_x, pix_y]

    def setLeftPrivateCallBack(self, func, private):
        self.leftExternalCallBack = func
        self.leftExternalPrivateData = private

    def getLeftPrivateCallBack(self):
        return self.leftExternalCallBack, self.leftExternalPrivateData

    def setRightPrivateCallBack(self, func, private):
        self.rightExternalCallBack = func
        self.rightExternalPrivateData = private

    #placeholder for canvas onclick listener
    def leftClickCallback(self, event):
        print ("clicked at", event.x, event.y)
        x,y = self.getHexForPix(event.x, event.y)
        if x >= 0 and y >= 0: 
            if (self.leftExternalCallBack is not None):
                self.leftExternalCallBack(self.leftExternalPrivateData, x, y)

    #placeholder for canvas onclick listener
    def rightClickCallback(self, event):
        print ("clicked at", event.x, event.y)
        x,y = self.getHexForPix(event.x, event.y)
        if x >= 0 and y >= 0: 
            if (self.rightExternalCallBack is not None):
                self.rightExternalCallBack(self.rightExternalPrivateData,
                                           event.x_root, event.y_root,
                                           x, y)

    def getHexForPix(self, x, y):
            #who am I closest to? guess.
            x_guess = int(x/ (2 * self.Δx))
            y_guess = int(y / (1.5 * self.hexaSize))
            print ("probably hex ", x_guess, y_guess)
            #Who surrounds that hex? (They don't have to be real!)
            guess = (x_guess,y_guess)
            x_pix,y_pix = self.findPixel(x_guess,y_guess)
            error = (x_pix - x)**2 + (y_pix - y)**2
            for neighbor in [((y_guess%2),1),(1,0),((y_guess%2),-1),
                    (y_guess%2-1,-1),(-1,0),(y_guess%2-1,1)]:
                x_curr = x_guess + neighbor[0]
                y_curr = y_guess + neighbor[1]
                #Which one am I closest to? measure!
                #find the pixel location
                x_pix,y_pix = self.findPixel(x_curr,y_curr)
                #pythagoras to the rescue!
                if (error > (x - x_pix)**2 + (y - y_pix)**2):
                    guess = (x_curr, y_curr)
                    error = (x - x_pix)**2 + (y - y_pix)**2
            #Am I real?
            if (guess[0] >= 0 and guess[0] < self.grid_width and
                    guess[1] >= 0 and guess[1] < self.grid_height):
                return guess[0], guess[1]
            else:
                return -1,-1


    #placeholder for canvas Motion listener
    def Motion(self, event):
        self.lastX = event.x
        self.lastY = event.y

    #placeholder for canvas Enter listener
    def Enter(self, event):
        self.bind("<Motion>", self.Motion)
        self.lastX = -1
        self.lastY = -1

    #placeholder for canvas Enter listener
    def Leave(self, event):
        self.unbind("<Motion>")
        self.lastX = -1
        self.lastY = -1

    def getCurrentPoint(self):
        return self.lastX, self.lastY

    def setBorders(self, x, y, color, width=2):
                        self.setCell(x, y,
                                            fill=None,
                                            color1=color,
                                            color2=color,
                                            color3=color,
                                            color4=color,
                                            color5=color,
                                            color6=color,
                                            width=width)
