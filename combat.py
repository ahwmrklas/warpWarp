# Pop up a dialog box that Permits selection of combat options
# Need a list of friendly ships and enemy ships.
# Need to be able to select a ship and make allocations and select targets
# Need a similar dialog to handle results. Report Damage inflicted and received
# and allocate damage to the required ships.

import tkinter as tk
from tkinter.simpledialog import *

class combat(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, friendlyList, enemyList):
        self.friendlyList = friendlyList
        self.enemyList = enemyList
        Dialog.__init__(self, master)

    # PURPOSE:
    # RETURNS:
    def targetList(self, shipFrame, enemyList):
        targetList = []
        for ship in enemyList:
            targetList.append(ship["name"])

        tmp = Label(shipFrame, text="Target: ")
        tmp.pack()

        if (len(targetList) > 0):
            targetVar = StringVar(shipFrame)
            targetVar.set("choose")
            target = OptionMenu(shipFrame, targetVar, *targetList)
            target.pack()

        # since this is called multiple times I assume I need
        # to record something so I know which
        # target selector is which. (which tube? or beam?)
        # So this will probably change. This is really just
        # a reminder return
        return targetVar

    # PURPOSE:
    # RETURNS:
    def singleShip(self, base, ship, enemyList):
        if not ship:
            return

        print(ship)

        shipFrame = LabelFrame(base,
                               text=ship['name'],
                               bg="orange", bd=1, relief="sunken")
        shipFrame.pack(fill=BOTH, expand=1)

        # Shrink the image (and I needed self.photo instead of photo
        # Something online suggested a tk bug?)
        self.photo = tk.PhotoImage(file="resource/images/" + ship['image'])
        #self.photo = self.photo.subsample(int(self.photo.width()/200))
        w = Canvas(shipFrame, width=50, height=50)
        w.create_image((0,0), image=self.photo)
        w.pack(expand=True, fill=BOTH)

        CurPD = ship['PD']['cur']
        text = "PowerDrive:" + str(CurPD) + " of " + str(ship['PD']['max'])
        tmp = Label(shipFrame, text=text)
        tmp.pack()

        tacticVar = StringVar(shipFrame)
        tacticVar.set("choose")

        tmp = Label(shipFrame, text="Move")
        tmp.pack()
        Drive = Spinbox(shipFrame, from_=0, to=CurPD)
        Drive.pack()

        CurB = ship['B']['cur']
        text = "Beams:" + str(CurB) + " of " + str(ship['B']['max'])
        tmp = Label(shipFrame, text=text)
        tmp.pack()
        Beams = Spinbox(shipFrame, from_=0, to=CurB)
        Beams.pack()

        CurS = ship['S']['cur']
        text = "Screens:" + str(CurS) + " of " + str(ship['S']['max'])
        tmp = Label(shipFrame, text=text)
        tmp.pack()
        Screens = Spinbox(shipFrame, from_=0, to=CurS)
        Screens.pack()

        CurM = ship['M']['cur']
        text = "Missiles:" + str(CurM) + " of " + str(ship['M']['max'])
        tmp = Label(shipFrame, text=text)
        tmp.pack()

        MaxT = ship['T']['max']
        CurT = ship['T']['cur']
        # Can't fire more tubes than missiles (or PD)
        CurT = min(CurT, CurM, CurPD)
        Tubes = []
        for i in range(0, CurT):
            tmp = Label(shipFrame, text="Tube_" + str(i+1))
            tmp.pack()
            Tubes.append(Spinbox(shipFrame, from_=0, to=99))
            Tubes[i].pack()
            self.targetList(shipFrame, enemyList)

        # User feedback showing all their tubes can't be used
        for i in range(CurT, MaxT):
            tmp = Label(shipFrame, text="Tube_" + str(i+1))
            tmp.pack()
            Tubes.append(Spinbox(shipFrame,
                                 from_=0, to=99, state = DISABLED))
            Tubes[i].pack()

        tacticList = ["attack", "dodge", "retreat"]
        tactic = OptionMenu(shipFrame, tacticVar, *tacticList)
        tactic.pack()

        self.targetList(shipFrame, enemyList)

    # PURPOSE: Override base class so we don't display any buttons
    # RETURNS:
    #def buttonbox(self):
    #    pass

    # PURPOSE:
    # RETURNS:
    def body(self, master):

        master.pack(fill=BOTH, expand=1)

        panes = tk.PanedWindow(master, orient="horizontal")
        panes.pack(fill=BOTH, expand=1)
        #panes.grid_rowconfigure(0, weight = 1)
        #panes.grid_columnconfigure(0, weight = 1)

        leftFrame = Frame(panes, bg="green", bd=1, relief="sunken")
        leftFrame.pack(expand=1, fill=BOTH)

        rightFrame = Frame(panes, bg="red", bd=1, relief="sunken")
        rightFrame.pack(expand=1, fill=BOTH)

        #panes.paneconfigure(leftFrame, stretch="always")
        #panes.paneconfigure(rightFrame, stretch="always")

        panes.add(leftFrame, stretch="always")
        panes.add(rightFrame, stretch="always")
        #panes.paneconfigure(leftFrame)
        

        redbutton = Button(rightFrame, text="Red", fg="red")
        redbutton.pack(expand=True, fill=BOTH)

        for entry in self.friendlyList:
            self.singleShip(leftFrame, entry, self.enemyList)

        return leftFrame # initial focus

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("nothing to apply")
