import tkinter as tk
from tkinter.simpledialog import *


class loadCargoMenu(Dialog):
    def __init__(self, master, star, ship):
        self.star = star
        self.ship = ship
        self.shipment = 0
        Dialog.__init__(self, master)

    def body(self, master):
        Label(master, text="Positive to Harvest, negative to deliver").grid()
        maxHaul = min([self.ship['H']['cur']*10 - self.ship['Hauled'], self.star['BP']['cur']])
        self.cargoSpinner = Spinbox(master, from_=0-self.ship['Hauled'], to_=maxHaul)
        self.cargoSpinner.grid()

    def apply(self):
        self.shipment = self.cargoSpinner.get()
