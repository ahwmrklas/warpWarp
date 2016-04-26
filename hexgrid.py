from tkinter import *
from xbm import TileContent
from xbm import TileFiles

# HexaCanvas inherits from Canvas
class HexaCanvas(Canvas):
    """ A canvas that provides a create-hexagone method """
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.hexaSize = 20

    def setHexaSize(self, number):
        self.hexaSize = number


    def create_hexagone(self, x, y, content = TileContent.NO_ITEMS,
            color = "black", fill="blue",
            color1=None, color2=None, color3=None, color4=None, color5=None,
            color6=None):
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
        Δx = (size**2 - (size/2)**2)**0.5

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

        self.create_line(point1, point2, fill=color1, width=2)
        self.create_line(point2, point3, fill=color2, width=2)
        self.create_line(point3, point4, fill=color3, width=2)
        self.create_line(point4, point5, fill=color4, width=2)
        self.create_line(point5, point6, fill=color5, width=2)
        self.create_line(point6, point1, fill=color6, width=2)

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

        HexaCanvas.__init__(self, master, background='white', width=width, height=height, *args, **kwargs)
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

    #PURPOSE: Draw a star on top of a hex grid
    #RETURNS: Nothing
    def drawStar(self, xCell, yCell):
        offset = self.hexaSize * 3 / 4

        #compute pixel coordinate of the center of the cell:
        [pix_x, pix_y] = self.findPixel(xCell, yCell)
        #self.create_oval(pix_x - offset, pix_y - offset,
        #                    pix_x + offset, pix_y + offset,
        #                    fill="yellow")
        self.photo = PhotoImage(file="resource/images/alpha.gif")
        self.photo = self.photo.subsample(int(self.photo.width()/self.hexaSize))
        self.create_image(pix_x,pix_y,image=self.photo)

    #PURPOSE: display the star objects
    #RETURNS: Nothing
    def drawStars(self, starlist):
        for star in starlist:
            x = star['location']['x']
            y = star['location']['y']
            self.drawStar(x,y)


    def findPixel(self, xCell, yCell):
        size = self.hexaSize
        Δx = (size**2 - (size/2)**2)**0.5

        pix_x = Δx + 2*Δx*xCell
        if yCell%2 ==1 :
            pix_x += Δx

        pix_y = size + yCell*1.5*size
        return [pix_x, pix_y]

