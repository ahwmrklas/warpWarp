# Pop up a dialog box that Permits selection of combat options
# Need a list of friendly ships and enemy ships.
# Need to be able to select a ship and make allocations and select targets
# Need a similar dialog to handle results. Report Damage inflicted and received
# and allocate damage to the required ships.

import tkinter as tk
from tkinter import ttk
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
    def shipInfo(self, tree, entry):
        if (entry['WG']['max']):
            text  =  "Warp" + entry['type']
            if (not entry['WG']['cur']):
                text  +=  "(Drive Currently Damaged)"
        else:
            text  =  "System" + entry['type']

        title = "techLevel " + str(entry['techLevel'])
        text1  =  "Moves left: " + str(entry['moves']['cur'])
        text2  =  "PowerDrive: " +  str(entry['PD']['cur']) + "(" + str(entry['PD']['max']) + ")"
        text2 +=  ", "
        text2 +=  "Shields " +  str(entry['S']['cur']) + "(" + str(entry['S']['max']) + ")"
        text3  =  "SystemRacks: " +  str(entry['SR']['cur']) + "(" + str(entry['SR']['max']) + ")"
        text3 +=  ", "
        text3 +=  "Beams: " +  str(entry['B']['cur']) + "(" + str(entry['B']['max']) + ")"
        text4  =  "Tubes: " +  str(entry['T']['cur']) + "(" + str(entry['T']['max']) + ")"
        text4 +=  " - "
        text4 +=  "Missiles: " +  str(entry['M']['cur']) + "(" + str(entry['M']['max']) + ")"
        base = tree.insert("", 'end', image=self.photo,
                           text=entry['name'],
                           values=[entry['owner'], text])
        line = tree.insert(base, 'end',
                           text=title,
                           values=["", text1])
        line = tree.insert(base, 'end',
                           text="",
                           values=["", text2])
        line = tree.insert(base, 'end',
                           text="",
                           values=["", text3])
        line = tree.insert(base, 'end',
                           text="",
                           values=["", text4])

    # PURPOSE: Override base class so we don't display any buttons
    # RETURNS:
    #def buttonbox(self):
    #    pass

    # PURPOSE:
    # RETURNS:
    def body(self, master):

        panes = ttk.PanedWindow(master, orient="horizontal")
        panes.pack(fill=BOTH, expand=True)
        panes.grid_rowconfigure(0, weight = 1)
        panes.grid_columnconfigure(0, weight = 1)

        leftFrame = Frame(panes, bg="green", bd=1, relief="sunken")
        leftFrame.pack(expand=True, fill=BOTH)

        rightFrame = Frame(panes, bg="red", bd=1, relief="sunken")
        rightFrame.pack(expand=True, fill=BOTH)

        panes.add(leftFrame, weight=1)
        panes.add(rightFrame, weight=1)

        #panes.paneconfig(leftFrame, width=120, sticky = "nsew")
        

        redbutton = Button(rightFrame, text="Red", fg="red")
        redbutton.pack(expand=True, fill=BOTH)

        for entry in self.friendlyList:
            if entry:
                print(entry)

                shipFrame = LabelFrame(leftFrame, text=entry['name'], bg="orange", bd=1, relief="sunken")
                shipFrame.pack()

                # Shrink the image (and I needed self.photo instead of photo
                # Something online suggested a tk bug?)
                self.photo = tk.PhotoImage(file="resource/images/" + entry['image'])
                #self.photo = self.photo.subsample(int(self.photo.width()/200))
                w = Canvas(shipFrame, width=50, height=50)
                w.create_image((0,0), image=self.photo)
                w.pack(expand=True, fill=BOTH)

                CurPD = entry['PD']['cur']
                text = "PowerDrive:" + str(CurPD) + " of " + str(entry['PD']['max'])
                PD = Label(shipFrame, text=text)
                PD.pack()

                tacticVar = StringVar(shipFrame)
                tacticVar.set("choose")

                Drive = Spinbox(shipFrame, from_=0, to=CurPD)
                Drive.pack()

                tactic = OptionMenu(shipFrame, tacticVar, "attack", "dodge", "retreat")
                tactic.pack()

              #  if entry['type'] == 'ship':
              #      self.shipInfo(tree, entry)

        return leftFrame # initial focus

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("nothing to apply")
