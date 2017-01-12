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

        if (len(targetList) > 0):
            targetVar = StringVar(shipFrame)
            targetVar.set("target")
            target = OptionMenu(shipFrame, targetVar, *targetList)

        # since this is called multiple times I assume I need
        # to record something so I know which
        # target selector is which. (which tube? or beam?)
        # So this will probably change. This is really just
        # a reminder return
        return target

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
        #self.photo = tk.PhotoImage(file="resource/images/" + "b_5.png")
        self.photo = tk.PhotoImage(file="resource/images/" + ship['image'])
        self.photo = self.photo.zoom(3)
        #self.photo = self.photo.subsample(int(self.photo.width()/200))
        w = Canvas(shipFrame, relief=SUNKEN, width='6c', height='4c', bg="pink")
        scaleW = int(self.photo.width()/w.winfo_reqwidth())
        scaleH = int(self.photo.height()/w.winfo_reqheight())
        self.photo = self.photo.subsample(scaleW, scaleH)
        w.create_image(0,0, anchor=NW, image=self.photo)
        w.pack(fill=BOTH, expand=1)

        CurPD = ship['PD']['cur']
        text = "PowerDrive:" + str(CurPD) + " of " + str(ship['PD']['max'])
        powerFrame = LabelFrame(shipFrame,
                                 text=text,
                                 bg="blue", bd=1, relief="sunken")
        powerFrame.pack(fill=BOTH, expand=1)

        tacticVar = StringVar(powerFrame)
        tacticVar.set("tactic")

        tmp = Label(powerFrame, text="Move")
        tmp.grid(row=2, column=0)
        Drive = Spinbox(powerFrame, width=3, from_=0, to=CurPD)
        Drive.grid(row=2, column=1)

        CurB = ship['B']['cur']
        text = "Beams:" + str(CurB) + " of " + str(ship['B']['max'])
        tmp = Label(powerFrame, text=text)
        tmp.grid(row=3, column=0)
        Beams = Spinbox(powerFrame, width=3, from_=0, to=CurB)
        Beams.grid(row=3, column=1)

        tmp = Label(powerFrame, text="Target: ")
        tmp.grid(row=3, column=2)
        target = self.targetList(powerFrame, enemyList)
        target.grid(row=3, column=3)

        CurS = ship['S']['cur']
        text = "Screens:" + str(CurS) + " of " + str(ship['S']['max'])
        tmp = Label(powerFrame, text=text)
        tmp.grid(row=4, column=0)
        Screens = Spinbox(powerFrame, width=3, from_=0, to=CurS)
        Screens.grid(row=4, column=1)

        tacticList = ["attack", "dodge", "retreat"]
        tactic = OptionMenu(powerFrame, tacticVar, *tacticList)
        tactic.grid(row=5, column=0)

        CurM = ship['M']['cur']
        text = "Missiles:" + str(CurM) + " of " + str(ship['M']['max'])
        missleFrame = LabelFrame(shipFrame,
                                 text=text,
                                 bg="blue", bd=1, relief="sunken")
        missleFrame.pack(fill=BOTH, expand=1)

        MaxT = ship['T']['max']
        CurT = ship['T']['cur']
        # Can't fire more tubes than missiles (or PD)
        CurT = min(CurT, CurM, CurPD)
        Tubes = []
        for i in range(0, CurT):
            tmp = Label(missleFrame, text="Tube_" + str(i+1))
            tmp.grid(row=i, column=0)
            Tubes.append(Spinbox(missleFrame, width=3, from_=0, to=99))
            Tubes[i].grid(row=i, column=1)
            tmp = Label(missleFrame, text="Target: ")
            tmp.grid(row=i, column=2)
            target = self.targetList(missleFrame, enemyList)
            target.grid(row=i, column=3)

        # User feedback showing all their tubes can't be used
        for i in range(CurT, MaxT):
            tmp = Label(missleFrame, text="Tube_" + str(i+1))
            tmp.grid(row=i, column=0)
            Tubes.append(Spinbox(missleFrame,
                                 width=3, from_=0, to=99, state = DISABLED))
            Tubes[i].grid(row=i, column=1)

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
