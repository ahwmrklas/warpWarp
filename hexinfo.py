# Pop up a dialog bog that displays all of the information about a particular
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
        tree.column('#0', width=150)
        tree.column('Owner', width=80)
        tree.column('Description', width=200)

        tree.grid(row=0)
        for entry in self.objList:
            if entry:
                print(entry)

                # Shrink the image (and I needed self.photo instead of photo
                # Something online suggested a tk bug?)
                self.photo = tk.PhotoImage(file="resource/images/" + entry['image'])
                self.photo = self.photo.subsample(int(self.photo.width()/20))

                base = tree.insert("", 'end', image=self.photo,
                                   text=entry['name'],
                                   values=[entry['owner'], entry['type']])
                if entry['type'] == 'ship':
                    title = "techLevel " + str(entry['techLevel'])
                    text1 =  "Moves left: " + str(entry['moves']['cur'])
                    text2 =  "PD: " +  str(entry['PD']['cur']) + "(" + str(entry['PD']['max']) + ")"
                    line = tree.insert(base, 'end',
                                       text=title,
                                       values=["", text1])
                    line = tree.insert(base, 'end',
                                       text="",
                                       values=["", text2])

        return tree # initial focus

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("nothing to apply")
