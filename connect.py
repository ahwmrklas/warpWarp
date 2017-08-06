# Dialog to connect to game server

import tkinter as tk
from tkinter.simpledialog import *
from client import comThrd
from cmds import warpWarCmds
import time

class connect(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, defaultName, defaultIP, defaultPort):
        self.name = StringVar()
        self.name.set(defaultName)
        self.startBases = StringVar()
        self.startBases.set("Ur Mosul Larsu") #Someday be a drop downlist
        self.startBaseList = ["Ur Mosul Larsu", "Nineveh Babylon Ugarit"]
        self.color = StringVar()
        self.color.set("Red")
        self.ip = StringVar()
        self.ip = StringVar()
        self.ip.set(defaultIP)
        self.port = IntVar()
        self.port.set(defaultPort)
        self.client = None
        Dialog.__init__(self, master)

    # PURPOSE:
    # RETURNS:
    def body(self, master):

        master.pack(fill=BOTH, expand=1)

        tmp = Label(master, text="PlayerName")
        tmp.pack()

        tmp = tk.Entry(master, textvariable=self.name)
        tmp.pack()

        tmp = Label(master, text="PlayerColor")
        tmp.pack()

        tmp = tk.Entry(master, textvariable=self.color)
        tmp.pack()

        tmp = Label(master, text="PlayerBases")
        tmp.pack()

        tmp = tk.OptionMenu(master, self.startBases, *self.startBaseList)
        tmp.pack()

        tmp = Label(master, text="SeverIP")
        tmp.pack()

        tmp = tk.Entry(master, textvariable=self.ip)
        tmp.pack()

        tmp = Label(master, text="Port")
        tmp.pack()

        tmp = tk.Entry(master, textvariable=self.port)
        tmp.pack()

        return tmp # initial focus

    # PURPOSE:
    # RETURNS:
    def validate(self):
        print("IP   ", self.ip.get())
        print("PORT ", self.port.get())
        tmp = warpWarCmds().ping('connectDlg')
        self.client = comThrd(self.ip.get(), self.port.get())
        self.client.sendCmd(tmp)
        resp = self.client.waitFor(5)

        print("RESP:", len(resp))
        if (len(resp) > 0):
            return True
        else:
            return False

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("return the client")
        self.result = self.client
        self.playerName = self.name.get()
        tmp = self.startBases.get()
        self.playerStartBases = tmp.split()
        self.playerColor = self.color.get()
