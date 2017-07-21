# Pop up a dialog box that displays all of the information about a particular
# location on the hex grid.
# Must give the location (the x,y or some sort of class with all the
# hex info?) And of course must give the info

import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import *

class hexInfo(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, objList):
        self.objList = objList
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

        tree = ttk.Treeview(master, columns=['Owner', 'Description'])
        tree.heading('#0', text='Name', anchor=tk.W)
        tree.heading('Owner', text='Owner', anchor=tk.W)
        tree.heading('Description', text='Description', anchor=tk.W)
        tree.column('#0', width=140)
        tree.column('Owner', width=70)
        tree.column('Description', width=220)

        tree.grid(row=0)
        for entry in self.objList:
            if entry:
                print(entry)

                # Shrink the image (and I needed self.photo instead of photo
                # Something online suggested a tk bug?)
                self.photo = tk.PhotoImage(file="resource/images/" + entry['image'])
                self.photo = self.photo.subsample(int(self.photo.width()/20))

                if entry['type'] == 'ship':
                    self.shipInfo(tree, entry)
                else:
                    base = tree.insert("", 'end', image=self.photo,
                                       text=entry['name'],
                                       values=[entry['owner'], entry['type']])

        return tree # initial focus

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("nothing to apply")
