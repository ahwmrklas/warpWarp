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
        self.combatOrders = dict((friend['name'], {}) for friend in friendlyList)
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
        print("disableBeamAndScreen")
        for w in self.energyFrame.winfo_children():
            w.configure(state="disable")

    # PURPOSE: Knowing how many and which tubes can be enabled is very
    #          tricky.
    #     don't enable tubes which are damaged
    #     only enable enough tubes for the # of missiles we have
    #     only enable enough tubes that we can power
    #       So if available power goes down (more power was used to move)
    #       we need to pick a tube to disable ... well, we better not pick
    #       a tube that is already in use!
    #         
    # RETURNS:
    def enableTubes(self):
        print("enableTubes")
        available = self.availablePower()
        usedT = self.getTubesUsed()

        CurM  = self.ship['M']['cur'] # # of missiles available
        MaxT  = self.ship['T']['max'] # Total tubes, even damaged
        CurT  = self.ship['T']['cur'] # current undamaged tubes

        tubesToEnable = min(CurT, CurM, available+usedT)
        if (usedT > tubesToEnable):
            print("ERROR:", usedT, ">", tubesToEnable)
            assert()

        tubesToDisable = MaxT - tubesToEnable
        print(" To Enable", tubesToEnable)
        print(" To Disable", tubesToDisable)

        # We shouldn't re-enable ALL of the tubes
        # check .functionalTube
        for tube in reversed(self.Tubes):
            if ((tubesToDisable > 0) and (tube.var.get() <= 0)):
                tubesToDisable -= 1
                tube.configure(state="disabled")
                tube.label.configure(state="disabled")
                tube.target.configure(state="disabled")
            else:
                tubesToEnable -= 1
                tube.configure(state="readonly")
                tube.label.configure(state="normal")
                tube.target.configure(state="normal")

        if (tubesToEnable != 0):
            print("Error tubesToEnable != 0", tubesToEnable )
        if (tubesToDisable != 0):
            print("Error tubesToDisable != 0", tubesToDisable )

    # PURPOSE:
    # RETURNS:
    def disableTubes(self):
        print("disableTubes")
        for w in self.missleFrame.winfo_children():
            w.configure(state="disable")

    # PURPOSE:
    # RETURNS:
    def availablePower(self):
        CurPD = self.ship['PD']['cur']
        usedPD = self.getPowerUsed()
        available = CurPD - usedPD
        return available

    # PURPOSE:
    # RETURNS:
    def recalculateRanges(self):
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
            usedT = self.getTubesUsed()
        except AttributeError:
            print("Missing member. Do nothing.")
        print("recalculate valid ranges")
        available = self.availablePower()
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
    def allUpdate(self, name, index, mode):
        print("allUpdate")
        self.updatePowerDrive()
        self.updateMissiles()
        self.recalculateRanges()
        if ((self.beamVar.get() > 0) or (self.screenVar.get() > 0)):
            self.enableBeamAndScreen()
            self.disableTubes()
        else:
            self.enableTubes()

            # If ANY Tube is in use, disable Beams
            for tube in self.Tubes:
                if (tube.var.get() > 0):
                    self.disableBeamAndScreen()
                    return

            self.enableBeamAndScreen()

    # PURPOSE: Create drop down list of potential targets
    # RETURNS: Return handle to created drop down list
    def createTargetList(self, shipFrame, enemyList, targetVar):
        targetList = []
        for ship in enemyList:
            targetList.append(ship["name"])

        targetVar.set("target")
        target = OptionMenu(shipFrame, targetVar, *targetList if targetList else "<NoEnemies>")

        return target

    # PURPOSE:
    # RETURNS:
    def getTubesUsed(self):
        usedT = 0
        try:
            for tube in self.Tubes:
                if (tube.var.get() > 0):
                    usedT = usedT + 1
        except AttributeError:
            print("Missing tubes. Do nothing.")
        return usedT

    # PURPOSE:
    # RETURNS:
    def getPowerUsed(self):
        usedPD = 0
        try:
            usedPD = usedPD + self.moveVar.get()
            usedPD = usedPD + self.screenVar.get()
            usedPD = usedPD + self.beamVar.get()
            usedPD = usedPD + self.getTubesUsed()
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

        firing = self.getTubesUsed()

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

        self.tacticVar = StringVar(self.powerFrame)
        self.tacticVar.set("tactic")
        tacticList = ["ATTACK", "DODGE", "RETREAT"]
        tactic = OptionMenu(self.powerFrame, self.tacticVar, *tacticList)
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

        self.beamTargetVar = StringVar(self.energyFrame)
        target = self.createTargetList(self.energyFrame, enemyList, self.beamTargetVar)
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
        self.Tubes = []
        for i in range(0, MaxT):
            tmp = Spinbox(self.missleFrame,
                          width=3, from_=0, to=99
                         )
            tmp.grid(row=i, column=1)
            self.Tubes.append(tmp)

            tmp = Label(self.missleFrame, text="Tube_" + str(i+1))
            tmp.grid(row=i, column=0, sticky="W")
            self.Tubes[i].label = tmp

            tmp = IntVar(self.missleFrame)
            tmp.set(0)
            tmp.trace("w", self.allUpdate)
            self.Tubes[i].var = tmp

            self.Tubes[i].targetVar = StringVar(self.missleFrame)
            tmp = self.createTargetList(self.missleFrame, enemyList, self.Tubes[i].targetVar)
            tmp.grid(row=i, column=2)
            self.Tubes[i].target = tmp

            self.Tubes[i].configure(textvariable=self.Tubes[i].var)

        # Figure out which of those tubes to enable/disable
        self.enableTubes()

        # Begin Trace late. (After all objects are instantiated)
        self.moveVar.trace("w", self.allUpdate)
        self.beamVar.trace("w", self.allUpdate)
        self.screenVar.trace("w", self.allUpdate)

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

        self.leftFrame = Frame(panes, bg="green", bd=1, relief="sunken")
        self.leftFrame.pack(expand=1, fill=BOTH)

        rightFrame = Frame(panes, bg="red", bd=1, relief="sunken")
        rightFrame.pack(expand=1, fill=BOTH)

        #panes.paneconfigure(self.leftFrame, stretch="always")
        #panes.paneconfigure(rightFrame, stretch="always")

        panes.add(self.leftFrame, stretch="always")
        panes.add(rightFrame, stretch="always")
        #panes.paneconfigure(self.leftFrame)
        

        redbutton = Button(rightFrame, text="Give order", fg="red", command = self.giveOrder)
        redbutton.pack(expand=True, fill=BOTH)

        self.shipSelectVar = StringVar(self.leftFrame)
        self.shipSelect = OptionMenu(self.leftFrame, self.shipSelectVar, 
                *[friendly['name'] for friendly in self.friendlyList],
                command=self.shipChange)
        self.shipSelectVar.set(self.friendlyList[0]['name'])
        self.shipSelect.pack(expand=True, fill=BOTH)

        self.shipFrame = Frame(self.leftFrame, bg="green")
        self.shipFrame.pack(expand=1, fill=BOTH)
        self.singleShip(self.shipFrame, self.friendlyList[0], self.enemyList)

        return self.leftFrame # initial focus

    def shipChange(self, name):
        print ("this is a stupid function, and the ship name is %s" % name)
        #we need to shake off self.shipFram
        self.shipFrame.destroy()
        self.shipFrame = Frame(self.leftFrame, bg="green")
        self.shipFrame.pack(expand=1, fill=BOTH)
        #find our ship!
        for ship in self.friendlyList:
            if ship['name'] == name:
                self.singleShip(self.shipFrame, ship, self.enemyList)
                break

    def giveOrder(self):

        #lets print out all the energy we are using!
        self.combatOrders[self.ship['name']] =   {
                        'ship'    : self.ship['name'], #TODO make this work for more than one ship
                        'tactic'  : [self.tacticVar.get(), self.moveVar.get()],
                        'beams'   : [self.beamTargetVar.get(),self.beamVar.get()],
                        'screens' : self.screenVar.get(),
                        'missiles' : [ [self.Tubes[i].targetVar.get(), self.Tubes[i].var.get()] for i in range(len(self.Tubes)) ]
                }

        print (self.combatOrders)

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("nothing to apply")

