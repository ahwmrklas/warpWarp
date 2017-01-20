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
    def enableBeamAndScreen(self):
        print("enableBeamAndScreen")
        for w in self.energyFrame.winfo_children():
            if (w.winfo_class() == "Spinbox"):
                w.configure(state="readonly")
            else:
                w.configure(state="normal")

    # PURPOSE:
    # RETURNS:
    def disableBeamAndScreen(self):
        for w in self.energyFrame.winfo_children():
            w.configure(state="disable")

    # PURPOSE:
    # RETURNS:
    def enableTubes(self):
        print("enableTubes")
        # We shouldn't re-enable ALL of the tubes
        # check .functionalTube
        for w in self.missleFrame.winfo_children():
            if (w.winfo_class() == "Spinbox"):
                if (w.functionalTube):
                    w.configure(state="readonly")
            else:
                w.configure(state="normal")

    # PURPOSE:
    # RETURNS:
    def disableTubes(self):
        for w in self.missleFrame.winfo_children():
            w.configure(state="disable")

    # PURPOSE:
    # RETURNS:
    def recalculateRages(self):
        CurPD = self.ship['PD']['cur']
        CurB  = self.ship['B']['cur']
        CurS  = self.ship['S']['cur']
        CurM  = self.ship['M']['cur']
        CurT  = self.ship['T']['cur']
        CurT = min(CurT, CurM, CurPD)
        usedPD = self.getPowerUsed()
        usedM = 0
        usedB = 0
        usedS = 0
        usedT = 0
        try:
            usedM = self.moveVar.get()
            usedB = self.beamVar.get()
            usedS = self.screenVar.get()
            for tube in self.Tubes:
                if (tube.var.get() > 0):
                    usedT = usedT + 1
        except AttributeError:
            print("Missing member. Do nothing.")
        print("recalculate valid ranges")
        available = CurPD - usedPD
        print("AVAIL: ", available)
        print("power", CurPD, "used: ", usedPD)
        print("move:", CurPD, "used: ", usedM, "new:", min(CurPD, available+usedM))
        print("CurB:", CurB, "used: ", usedB, "new:", min(CurB, available+usedB))
        print("CurS:", CurS, "used: ", usedS, "new:", min(CurS, available+usedS))
        print("CurT:", CurT, "used: ", usedT, "new:", min(CurT, available+usedT))
        print("CurM:", CurM)
        self.Move.configure(to=min(CurPD, available+usedM))
        self.Beams.configure(to=min(CurB, available+usedB))
        self.Screens.configure(to=min(CurS, available+usedS))

    # PURPOSE:
    # RETURNS:
    def moveTrace(self, name, index, mode):
        print("move trace ", self.moveVar.get())
        self.updatePowerDrive()
        self.recalculateRages()

    # PURPOSE:
    # RETURNS:
    def beamTrace(self, name, index, mode):
        print("beam trace ", self.beamVar.get())

        if ((self.beamVar.get() > 0) or (self.screenVar.get() > 0)):
            self.disableTubes()
        else:
            self.enableTubes()
        self.updatePowerDrive()
        self.recalculateRages()

    # PURPOSE:
    # RETURNS:
    def screenTrace(self, name, index, mode):
        print("screen trace ", self.screenVar.get())

        if (not self.beamVar):
            print("catch an error during destruction")
            return

        if ((self.beamVar.get() > 0) or (self.screenVar.get() > 0)):
            self.disableTubes()
        else:
            self.enableTubes()
        self.updatePowerDrive()
        self.recalculateRages()

    # PURPOSE:
    # RETURNS:
    def tubeTrace(self, i):
        print("tube trace ", i, self.Tubes[i].var.get())
        self.updatePowerDrive()
        self.updateMissiles()
        # If ANY Tube is in use, disable Beams
        for tube in self.Tubes:
            if (tube.var.get() > 0):
                self.disableBeamAndScreen()
                return

        self.enableBeamAndScreen()
        self.recalculateRages()

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
    def getPowerUsed(self):
        usedPD = 0
        try:
            usedPD = usedPD + self.moveVar.get()
            usedPD = usedPD + self.screenVar.get()
            usedPD = usedPD + self.beamVar.get()
            for tube in self.Tubes:
                if (tube.var.get() > 0):
                    usedPD = usedPD + 1
        except AttributeError:
            print("Missing member. Do nothing.")

        return usedPD

    # PURPOSE:
    # RETURNS:
    def updatePowerDrive(self):

        CurPD = self.ship['PD']['cur']
        text = ( "PowerDrive:"
                 + str(CurPD)
                 + " of "
                 + str(self.ship['PD']['max'])
                 + " Used: "
                 + str(self.getPowerUsed())
               )
        self.powerFrame.config(text=text)

    # PURPOSE:
    # RETURNS:
    def updateMissiles(self):

        firing = 0
        for tube in self.Tubes:
            if (tube.var.get() > 0):
                firing = firing + 1

        CurM = self.ship['M']['cur']
        text = ( "Missiles:"
                 + str(CurM)
                 + " of "
                 + str(self.ship['M']['max'])
                 + " Firing: "
                 + str(firing)
               )
        self.missleFrame.config(text=text)

    # PURPOSE:
    # RETURNS:
    def singleShip(self, base, ship, enemyList):
        if not ship:
            return

        self.ship = ship
        print(self.ship)

        shipFrame = LabelFrame(base,
                               text=ship['name'],
                               bg="orange", bd=1, relief="sunken")
        shipFrame.pack(fill=BOTH, expand=1)

        # Shrink the image (and I needed self.photo instead of photo
        # Something online suggested a tk bug?)
        self.photo = tk.PhotoImage(file="resource/images/" + ship['image'])
        self.photo = self.photo.zoom(3)
        w = Canvas(shipFrame, relief=SUNKEN, width='6c', height='4c', bg="pink")
        scaleW = int(self.photo.width()/w.winfo_reqwidth())
        scaleH = int(self.photo.height()/w.winfo_reqheight())
        self.photo = self.photo.subsample(scaleW, scaleH)
        w.create_image(0,0, anchor=NW, image=self.photo)
        w.pack(fill=BOTH, expand=1)

        CurPD = ship['PD']['cur']
        self.powerFrame = LabelFrame(shipFrame,
                                 text="PowerDrive",
                                 bg="blue", bd=1, relief="sunken")
        self.powerFrame.pack(fill=BOTH, expand=1)

        self.moveVar = IntVar(self.powerFrame)
        self.moveVar.set(0)
        tmp = Label(self.powerFrame, text="Move")
        tmp.grid(row=2, column=0, sticky="W")
        self.Move = Spinbox(self.powerFrame, width=3,
                       from_=0, to=CurPD,
                       textvariable=self.moveVar,
                       state = "readonly"
                      )
        self.Move.grid(row=2, column=1)

        tacticVar = StringVar(self.powerFrame)
        tacticVar.set("tactic")
        tacticList = ["attack", "dodge", "retreat"]
        tactic = OptionMenu(self.powerFrame, tacticVar, *tacticList)
        tactic.grid(row=2, column=2)

        self.energyFrame = LabelFrame(shipFrame,
                                 text="Energy Weapons",
                                 bg="blue", bd=1, relief="sunken")

        self.energyFrame.pack(fill=BOTH, expand=1)
        self.beamVar = IntVar(self.energyFrame)
        self.beamVar.set(0)
        CurB = ship['B']['cur']
        text = "Beams:" + str(CurB) + " of " + str(ship['B']['max'])
        tmp = Label(self.energyFrame, text=text)
        tmp.grid(row=3, column=0, sticky="W")
        self.Beams = Spinbox(self.energyFrame, width=3,
                             from_=0, to=CurB,
                             textvariable=self.beamVar,
                             state = "readonly"
                            )
        self.Beams.grid(row=3, column=1)

        target = self.targetList(self.energyFrame, enemyList)
        target.grid(row=3, column=2)

        self.screenVar = IntVar(self.energyFrame)
        self.screenVar.set(0)
        CurS = ship['S']['cur']
        text = "Screens:" + str(CurS) + " of " + str(ship['S']['max'])
        tmp = Label(self.energyFrame, text=text)
        tmp.grid(row=4, column=0, sticky="W")
        self.Screens = Spinbox(self.energyFrame, width=3,
                          from_=0, to=CurS,
                          textvariable=self.screenVar,
                          state = "readonly"
                         )
        self.Screens.grid(row=4, column=1)

        CurM = ship['M']['cur']
        self.missleFrame = LabelFrame(shipFrame,
                                 text="Missiles",
                                 bg="blue", bd=1, relief="sunken")
        self.missleFrame.pack(fill=BOTH, expand=1)

        MaxT = ship['T']['max']
        CurT = ship['T']['cur']
        # Can't fire more tubes than missiles (or PD)
        CurT = min(CurT, CurM, CurPD)
        self.Tubes = []
        for i in range(0, CurT):
            tmp = Label(self.missleFrame, text="Tube_" + str(i+1))
            tmp.grid(row=i, column=0, sticky="W")
            self.Tubes.append(tmp)

            self.Tubes[i].var = IntVar(self.missleFrame)
            self.Tubes[i].var.set(0)
            self.Tubes[i].var.trace("w", lambda n1, n2, op, i=i: self.tubeTrace(i))
            tmp = Spinbox(self.missleFrame,
                          width=3, from_=0, to=99,
                          textvariable=self.Tubes[i].var,
                          state = "readonly"
                         )
            tmp.functionalTube = True
            self.Tubes[i].spin = tmp
            self.Tubes[i].spin.grid(row=i, column=1)

            target = self.targetList(self.missleFrame, enemyList)
            target.grid(row=i, column=2)

        # User feedback showing all their tubes can't be used
        for i in range(CurT, MaxT):
            tmp = Label(self.missleFrame, text="Tube_" + str(i+1))
            tmp.grid(row=i, column=0, sticky="W")
            self.Tubes.append(tmp)

            tmp = Spinbox(self.missleFrame,
                          width=3, from_=0, to=99,
                          state = DISABLED
                         )
            tmp.functionalTube = False
            self.Tubes[i].spin = tmp
            self.Tubes[i].spin.grid(row=i, column=1)

        # Begin Trace late. (After all objects are instantiated)
        self.moveVar.trace("w", self.moveTrace)
        self.beamVar.trace("w", self.beamTrace)
        self.screenVar.trace("w", self.screenTrace)

        self.updatePowerDrive()
        self.updateMissiles()

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
