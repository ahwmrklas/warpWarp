# Pop up a dialog bog that displays all of the information about a particular
# location on the hex grid.
# Must give the location (the x,y or some sort of class with all the
# hex info?) And of course must give the info

from tkinter import *
from tkinter.simpledialog import *

class hexInfo(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, objList):
        self.objList = objList
        Dialog.__init__(self, master)

    # PURPOSE:
    # RETURNS:
    def body(self, master):

        for entry in self.objList:
            print(entry)
        Label(master, text="First:").grid(row=0)
        Label(master, text="Second:").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        return self.e1 # initial focus

    # PURPOSE:
    # RETURNS:
    def apply(self):
        first = int(self.e1.get())
        second = int(self.e2.get())
        print(first, second) # or something
