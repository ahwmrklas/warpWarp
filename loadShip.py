from connect import *
from cmds import warpWarCmds
import tkinter as tk
from tkinter.simpledialog import *

class loadShipMenu(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, ship, shipList):
        self.ship = ship
        self.shipList = shipList
        #TODO: what if hCon is null?
        self.location = [self.ship['location']['x'], self.ship['location']['y']]
        self.finished = 0 #should the caller use our result?
        Dialog.__init__(self, master)

    def body(self, master):
        #just a drop down list with ship names
        self.motherVar = StringVar(master)
        #but not any ships! only the ones in this hex
        motherList = [ship for ship in self.shipList if ship['location']['x'] == self.location[0] and ship['location']['y'] == self.location[1]]
        nameList = [ship['name'] for ship in motherList if ship['SR']['cur'] >= 1]
        if len(nameList) > 0:
            mother = OptionMenu(master, self.motherVar, 
                    *[ship['name'] for ship in motherList if ship['SR']['cur'] >= 1] + ["unload"])
            mother.grid()
        else:
            Label(master, text="No ships capable of carrying me!").grid()
            self.bind("<Return>", self.cancel)
            self.apply = self.cancel

    def apply(self):
        if self.motherVar.get():
            self.finished = 1

def findMother(listOfShips, child):
    for ship in listOfShips:
        print (ship)
        if child in ship['carried_ships']:
            return ship['name']
