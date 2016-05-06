#PURPOSE: a two dimensional array to populate with file names and params
#           to draw objects on the hexgrid
#PARAMS: x and y dimensions, and a game dictionary
class DrawArray():
    def __init__(self,x,y,game):
        self.array = [[["",0] for i in range(y)] for j in range(x)]
        self.makeDrawList(game['starList'])
        self.makeDrawList(game['thingList'])
        self.makeDrawList(game['shipList'])
        #self.drawWarpLines(game['WarpLineList'])
        self.makeDrawList(game['starBaseList'])

    #PURPOSE: display a list of objects
    #RETURNS: Nothing
    def makeDrawList(self, objectList):
        for obj in objectList:
            x = obj['location']['x']
            y = obj['location']['y']
            if self.array[x][y][0] != "":
                self.array[x][y][1] += 1
            self.array[x][y][0] = obj['image']

