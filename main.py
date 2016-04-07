# Main program for WarpWar
# More stuff will go here someday
# Right now there is no client/server
#
# Written with Python 3.4.2
#

# imports
from hexgrid import *
from tkinter import *
from xbm import TileContent

# PURPOSE: Button handler. The Quit button
#          call this when "Quit" button clicked
# RETURNS: I don't know.
def correct_quit(tk):
    tk.destroy()
    tk.quit()

# PURPOSE: Just make a function out of the main code. It doesn't
#          seem right without that.
# RETURNS: ?? hmmm
def main():

    # Instance of tkinter to do GUI stuff
    tk = Tk()

    # create a hex map that is the basis of our game display
    hexMap = HexagonalGrid(tk, scale = 20, grid_width=10, grid_height=10)

    # Locate the hexmap on the tkinter "grid"
    hexMap.grid(row=0, column=0, padx=10, pady=10)

    # Create a quit button (obviously to exit the program)
    quit = Button(tk, text = "Quit", command = lambda :correct_quit(tk))

    # Locate the button on the tkinter "grid"
    quit.grid(row=1, column=0)

    # display the whole hexMap. This should be moved in to a function inside hexMap
    for x in range(0, hexMap.grid_width):
        for y in range(0, hexMap.grid_height):
            hexMap.setCell(x,y, fill='yellow')

    #hexMap.setCell(0,0, fill='blue')
    #hexMap.setCell(1,0, fill='red')
    #hexMap.setCell(0,1, fill='green')
    #hexMap.setCell(1,1, fill='yellow')
    #hexMap.setCell(2,0, fill='cyan')
    #hexMap.setCell(0,2, fill='teal')
    #hexMap.setCell(2,1, fill='silver')
    #hexMap.setCell(1,2, fill='white')
    #hexMap.setCell(2,2, fill='gray')
    #hexMap.setCell(3,3, fill='fuchsia')

    hexMap.setCell(4,4, fill='pink', content=TileContent.BASIC_SHIP)

    # Let tkinter main loop run forever and handle input events
    tk.mainloop()

# Start the main function
if __name__ == "__main__":
   main()
