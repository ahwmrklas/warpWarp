
import tkinter as tk
from tkinter.simpledialog import *
import math

class build(Dialog):

    class _Spinbox(tk.Frame):
        def __init__(self, master, limit, callback):
            tk.Frame.__init__(self, master)
            self.limit = limit
            self.callback = callback

        def _grid(self, row=0, column=0):
            self.spinnerValue = tk.IntVar()
            self.text = tk.Label(self, text="0", textvariable=self.spinnerValue, width=5, anchor='e', relief='ridge', bg='white')
            self.text.grid(row=0, column=0)
            self.spinnerValue.set(0)
            self.upButton = tk.Button(self, text=u"\u25B2", bg='green', activebackground='green yellow',
                    font=('Times', 12, 'bold'), width=1, height=1, command=self.upPress)
            self.upButton.grid(row=0, column=1)
            self.downButton = tk.Button(self, text=u"\u25BC", bg='red4', activebackground='red',
                    font=('Times', 12, 'bold'), width=1, height=1, command=self.downPress)
            self.downButton.grid(row=0, column=2)
            self.grid(row=row, column=column)

        def upPress(self):
            self.spinnerValue.set(min(self.spinnerValue.get() + 1, self.limit))
            self.callback()

        def downPress(self):
            self.spinnerValue.set(max(self.spinnerValue.get() - 1, 0))
            self.callback()

        def get(self):
            return self.spinnerValue.get()

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, base):
        self.base = base
        self.ship = {}
        print(self.base['owner'])
        self.remaining = self.base['BP']['cur']
        Dialog.__init__(self, master)

    # PURPOSE:
    # RETURNS:
    def makeHeader(self, headerFrame):
        headerFrame.grid(columnspan=2)
        totalFrame = Frame(headerFrame, relief=RIDGE, bd=10)
        TotalW = Label(totalFrame, text="Total BP:%d" % self.base['BP']['cur'])
        TotalW.grid()
        totalFrame.grid(row=0,column=1)

        spentFrame = Frame(headerFrame, relief=RIDGE, bd=10)
        self.spentW = Label(spentFrame, text="Used BP:%d" % 0)
        self.spentW.grid()
        spentFrame.grid(row=0,column=2)

        remainingFrame = Frame(headerFrame, relief=RIDGE, bd=10)
        self.remainingW = Label(remainingFrame, text="Remaining BP:%d" % self.base['BP']['cur'])
        self.remainingW.grid()
        remainingFrame.grid(row=0,column=3)

    # PURPOSE:
    # RETURNS:
    def makeSpinners(self, spinFrame):
        self.spinList = []

        tmpLbl = Label(spinFrame, text="SHIP NAME")
        tmpLbl.grid(row=1, column=0)
        self.shipNameEntry = Entry(spinFrame)
        self.shipNameEntry.grid(row=1, column=1)

        tmpLbl = Label(spinFrame, text="POWER DRIVE")
        tmpLbl.grid(row=2, column=0)
        self.pwrSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.spinList.append(self.pwrSpn)
        self.pwrSpn._grid(row=2, column=1)

        tmpLbl = Label(spinFrame, text="BEAMS")
        tmpLbl.grid(row=3, column=0)
        self.beamSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.beamSpn._grid(row=3, column=1)
        self.spinList.append(self.beamSpn)

        tmpLbl = Label(spinFrame, text="SCREENS")
        tmpLbl.grid(row=4, column=0)
        self.screenSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.screenSpn._grid(row=4, column=1)
        self.spinList.append(self.screenSpn)

        tmpLbl = Label(spinFrame, text="ELECTRONIC COUNTERMEASURES")
        tmpLbl.grid(row=5, column=0)
        self.ecmSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.ecmSpn._grid(row=5, column=1)
        self.spinList.append(self.ecmSpn)

        tmpLbl = Label(spinFrame, text="TUBES")
        tmpLbl.grid(row=6, column=0)
        self.tubeSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.tubeSpn._grid(row=6, column=1)
        self.spinList.append(self.tubeSpn)

        tmpLbl = Label(spinFrame, text="MISSLES (x3)")
        tmpLbl.grid(row=7, column=0)
        self.mslSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.mslSpn._grid(row=7, column=1)
        self.spinList.append(self.mslSpn)

        tmpLbl = Label(spinFrame, text="ARMOR (x2)")
        tmpLbl.grid(row=8, column=0)
        self.armorSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.armorSpn._grid(row=8, column=1)
        self.spinList.append(self.armorSpn)

        tmpLbl = Label(spinFrame, text="CANNONS")
        tmpLbl.grid(row=9, column=0)
        self.cannonSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.cannonSpn._grid(row=9, column=1)
        self.spinList.append(self.cannonSpn)

        tmpLbl = Label(spinFrame, text="SHELLS (x6)")
        tmpLbl.grid(row=10, column=0)
        self.shellSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.shellSpn._grid(row=10, column=1)
        self.spinList.append(self.shellSpn)

        tmpLbl = Label(spinFrame, text="SYSTEMSHIP RACKS")
        tmpLbl.grid(row=11, column=0)
        self.srSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.srSpn._grid(row=11, column=1)
        self.spinList.append(self.srSpn)

        tmpLbl = Label(spinFrame, text="HOLDS")
        tmpLbl.grid(row=12, column=0)
        self.holdSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.holdSpn._grid(row=12, column=1)
        self.spinList.append(self.holdSpn)

        tmpLbl = Label(spinFrame, text="REPAIR BAYS (1/5 BP)")
        tmpLbl.grid(row=13, column=0)
        self.rpSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.rpSpn._grid(row=13, column=1)
        #self.spinList.append(self.rpSpn) we treat this one special

        tmpLbl = Label(spinFrame, text="WARP GENERATOR")
        tmpLbl.grid(row=14, column=0)
        self.warpSpn = self._Spinbox(spinFrame, self.remaining, self.updateSpinners)
        self.warpSpn._grid(row=14, column=1)

        spinFrame.grid()

    # PURPOSE:
    # RETURNS:
    def updateSpinners(self):
        used = 0
        for spinner in self.spinList:
            used = used + int(spinner.get())

        used = used + 5 * int(self.rpSpn.get())
        used = used + 5 * int(self.warpSpn.get())

        for spinner in self.spinList:
            spinner.limit=self.base['BP']['cur'] - used + int(spinner.get())

        self.rpSpn.limit = int((self.base['BP']['cur'] - used)/5) + int(self.rpSpn.get())

        self.spentW.config(text="Used BP:%d" % used)
        self.remainingW.config(text="Remaining BP:%d" % (self.base['BP']['cur'] - used))

    # PURPOSE:
    # RETURNS:
    def body(self, master):
        #have a bunch of spinboxes and checkboxes
        statusFrame = Frame(master)
        self.makeHeader(statusFrame)
        spinFrame = Frame(master)
        self.makeSpinners(spinFrame)

    # PURPOSE:
    # RETURNS:
    def validate(self):
        print("validate build")
        return True

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("apply build")
        print(self.base['owner'])
        moves = math.ceil(int(self.pwrSpn.get())/2)
        self.ship =  {
             'name': self.shipNameEntry.get(),
             'type': "ship",
             'location': {'x':self.base['location']['x'], 'y':self.base['location']['y']},
             'image':"ship1.png",
             'owner': self.base['owner'],
             'techLevel': 1,
             'damage': 0,
             'moves': {'max': moves, 'cur': moves},   # relates to PowerDrive
             'PD': {'max': int(self.pwrSpn.get()), 'cur': int(self.pwrSpn.get())},       # PowerDrive
             'WG': {'max': True if int(self.warpSpn.get()) == 1 else False, 'cur': True if int(self.warpSpn.get()) == 1 else False}, # Warp Generator
             'B': {'max':int(self.beamSpn.get()), 'cur':int(self.beamSpn.get())},       # Beams
             'S': {'max':int(self.screenSpn.get()), 'cur':int(self.screenSpn.get())},       # Screens (Shields)
             'E': {'max':int(self.ecmSpn.get()), 'cur':int(self.ecmSpn.get())},       # Electronic Counter Measures (New)
             'T': {'max':int(self.tubeSpn.get()), 'cur':int(self.tubeSpn.get())},       # Tubes
             'M': {'max':int(self.mslSpn.get()) * 3, 'cur':int(self.mslSpn.get()) * 3},       # Missiles
             'A': {'max':int(self.armorSpn.get()), 'cur':int(self.armorSpn.get())},       # Armor (New)
             'C': {'max':int(self.cannonSpn.get()), 'cur':int(self.cannonSpn.get())},       # Cannons (New)
             'SH':{'max':int(self.shellSpn.get()) * 6, 'cur':int(self.shellSpn.get()) * 6},       # Shells (New)
             'SR':{'max':int(self.srSpn.get()), 'cur':int(self.srSpn.get())},       # System Ship Racks
             'H': {'max':int(self.holdSpn.get()), 'cur':int(self.holdSpn.get())},       # Holds (New)
             'Hauled':0, #Are any BP being hauled?
             'R': {'max':int(self.rpSpn.get()), 'cur':int(self.rpSpn.get())},       # Repair Bays (New)
             'visibility':[ {'player':self.base['owner'],  'percent':10}],
             'carried_ships' :[],
            }
        print (self.ship)


