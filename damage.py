import tkinter as tk
from tkinter.simpledialog import *

# PURPOSE int() throws an error for an empty string. I want 0
# RETURNS: an integer
def myInt(string):
    if string.isdigit():
        return int(string)
    return 0

class damageAllocation(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, ship):
        self.ship = ship
        self.remaining = self.ship['damage']
        self.finished = 0
        Dialog.__init__(self, master)

    # PURPOSE:
    # RETURNS:
    def makeHeader(self, headerFrame):
        headerFrame.grid(columnspan=2)
        totalFrame = Frame(headerFrame, relief=RIDGE, bd=10)
        TotalW = Label(totalFrame, text="Total Damage:%d" % self.ship['damage'])
        TotalW.grid()
        totalFrame.grid(row=0,column=1)

        spentFrame = Frame(headerFrame, relief=RIDGE, bd=10)
        self.spentW = Label(spentFrame, text="Used Damage:%d" % 0)
        self.spentW.grid()
        spentFrame.grid(row=0,column=2)

        remainingFrame = Frame(headerFrame, relief=RIDGE, bd=10)
        self.remainingW = Label(remainingFrame, text="Remaining Damage:%d" % self.ship['damage'])
        self.remainingW.grid()
        remainingFrame.grid(row=0,column=3)

    # PURPOSE:
    # RETURNS:
    def makeSpinners(self, spinFrame):
        self.spinList = []

        tmpLbl = Label(spinFrame, text="SHIP NAME")
        tmpLbl.grid(row=1, column=0)
        self.shipNameLabel = Label(spinFrame, text=self.ship['name'])
        self.shipNameLabel.grid(row=1, column=1)

        tmpLbl = Label(spinFrame, text="POWER DRIVE: %d" %self.ship['PD']['cur'])
        tmpLbl.grid(row=2, column=0)
        self.pwrSpn = Spinbox(spinFrame, from_=0, to=self.ship['PD']['cur'], state="readonly", command=self.updateSpinners)
        self.pwrSpn.limit = self.ship['PD']['cur']
        self.spinList.append(self.pwrSpn)
        self.pwrSpn.grid(row=2, column=1)

        tmpLbl = Label(spinFrame, text="BEAMS: %d" % self.ship['B']['cur'])
        tmpLbl.grid(row=3, column=0)
        self.beamSpn = Spinbox(spinFrame, from_=0, to=self.ship['B']['cur'], state="readonly", command=self.updateSpinners)
        self.beamSpn.grid(row=3, column=1)
        self.beamSpn.limit = self.ship['B']['cur']
        self.spinList.append(self.beamSpn)

        tmpLbl = Label(spinFrame, text="SCREENS: %d" % self.ship['S']['cur'])
        tmpLbl.grid(row=4, column=0)
        self.screenSpn = Spinbox(spinFrame, from_=0, to=self.ship['S']['cur'], state="readonly", command=self.updateSpinners)
        self.screenSpn.grid(row=4, column=1)
        self.screenSpn.limit = self.ship['S']['cur']
        self.spinList.append(self.screenSpn)

        tmpLbl = Label(spinFrame, text="ELECTRONIC COUNTERMEASURES: %d" % self.ship['E']['cur'])
        tmpLbl.grid(row=5, column=0)
        self.ecmSpn = Spinbox(spinFrame, from_=0, to=self.ship['E']['cur'], state="readonly", command=self.updateSpinners)
        self.ecmSpn.grid(row=5, column=1)
        self.ecmSpn.limit = self.ship['E']['cur']
        self.spinList.append(self.ecmSpn)

        tmpLbl = Label(spinFrame, text="TUBES: %d" % self.ship['T']['cur'])
        tmpLbl.grid(row=6, column=0)
        self.tubeSpn = Spinbox(spinFrame, from_=0, to=self.ship['T']['cur'], state="readonly", command=self.updateSpinners)
        self.tubeSpn.grid(row=6, column=1)
        self.tubeSpn.limit = self.ship['T']['cur']
        self.spinList.append(self.tubeSpn)

        tmpLbl = Label(spinFrame, text="ARMOR (x2): %d" % self.ship['A']['cur'])
        tmpLbl.grid(row=8, column=0)
        self.armorSpn = Spinbox(spinFrame, from_=0, to=self.ship['A']['cur'], state="readonly", command=self.updateSpinners)
        self.armorSpn.grid(row=8, column=1)
        self.armorSpn.limit = self.ship['A']['cur']
        self.spinList.append(self.armorSpn)

        tmpLbl = Label(spinFrame, text="CANNONS: %d" % self.ship['C']['cur'])
        tmpLbl.grid(row=9, column=0)
        self.cannonSpn = Spinbox(spinFrame, from_=0, to=self.ship['C']['cur'], state="readonly", command=self.updateSpinners)
        self.cannonSpn.grid(row=9, column=1)
        self.cannonSpn.limit = self.ship['C']['cur']
        self.spinList.append(self.cannonSpn)

        tmpLbl = Label(spinFrame, text="SYSTEMSHIP RACKS: %d" % self.ship['SR']['cur'])
        tmpLbl.grid(row=11, column=0)
        self.srSpn = Spinbox(spinFrame, from_=0, to=self.ship['SR']['cur'], state="readonly", command=self.updateSpinners)
        self.srSpn.grid(row=11, column=1)
        self.srSpn.limit = self.ship['SR']['cur']
        self.spinList.append(self.srSpn)

        tmpLbl = Label(spinFrame, text="HOLDS: %d" % self.ship['H']['cur'])
        tmpLbl.grid(row=12, column=0)
        self.holdSpn = Spinbox(spinFrame, from_=0, to=self.ship['H']['cur'], state="readonly", command=self.updateSpinners)
        self.holdSpn.grid(row=12, column=1)
        self.holdSpn.limit = self.ship['H']['cur']
        self.spinList.append(self.holdSpn)

        tmpLbl = Label(spinFrame, text="REPAIR BAYS (1/5 BP): %d" % self.ship['R']['cur'])
        tmpLbl.grid(row=13, column=0)
        self.rpSpn = Spinbox(spinFrame, from_=0, to=int(self.remaining / 5), state="readonly", command=self.updateSpinners)
        self.rpSpn.grid(row=13, column=1)
        self.rpSpn.limit = self.ship['R']['cur']
        #self.spinList.append(self.rpSpn) we treat this one special

        tmpLbl = Label(spinFrame, text="WARP GENERATOR: %d" % self.ship['WG']['cur'])
        tmpLbl.grid(row=14, column=0)
        self.warpSpn = Spinbox(spinFrame, from_=0, to=1, state="readonly", command=self.updateSpinners)
        self.warpSpn.grid(row=14, column=1)

        spinFrame.grid()

    # PURPOSE:
    # RETURNS:
    def usedDamage(self):
        used = 0
        for spinner in self.spinList:
            used = used + myInt(spinner.get())

        used = used + 5 * myInt(self.rpSpn.get())
        used = used + 5 * myInt(self.warpSpn.get())

        return used


    # PURPOSE:
    # RETURNS:
    def updateSpinners(self):
        used = self.usedDamage()

        for spinner in self.spinList:
            if spinner.limit >= (self.ship['damage'] - used + myInt(spinner.get())):
                spinner.config(to=self.ship['damage'] - used + myInt(spinner.get()))

        self.rpSpn.config(to=int((self.ship['damage'] - used)/5) + myInt(self.rpSpn.get()))

        self.spentW.config(text="Used Damage:%d" % used)
        self.remainingW.config(text="Remaining Damage:%d" % (self.ship['damage'] - used))

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
        print("validate damage")
        return True

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("apply damage")
        self.ship['damage']  = self.ship['damage'] - self.usedDamage()
        self.ship['PD']['cur'] = self.ship['PD']['cur'] - myInt(self.pwrSpn.get())       # PowerDrive
        self.ship['B']['cur']  = self.ship['B']['cur']  - myInt(self.beamSpn.get())
        self.ship['S']['cur']  = self.ship['S']['cur']  - myInt(self.screenSpn.get())
        self.ship['E']['cur']  = self.ship['E']['cur']  - myInt(self.ecmSpn.get())
        self.ship['T']['cur']  = self.ship['T']['cur']  - myInt(self.tubeSpn.get())
        self.ship['A']['cur']  = self.ship['A']['cur']  - myInt(self.armorSpn.get())
        self.ship['C']['cur']  = self.ship['C']['cur']  - myInt(self.cannonSpn.get())
        self.ship['SR']['cur'] = self.ship['SR']['cur'] - myInt(self.srSpn.get())
        self.ship['H']['cur']  = self.ship['H']['cur']  - myInt(self.holdSpn.get())
        self.ship['R']['cur']  = self.ship['R']['cur']  - myInt(self.rpSpn.get())
        self.ship['WG']['cur'] = self.ship['WG']['cur'] - myInt(self.warpSpn.get())
        print (self.ship)
        self.finished = 1
