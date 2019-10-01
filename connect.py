# Dialog to connect to game server

import tkinter as tk
from tkinter.simpledialog import *
from client import comThrd
from cmds import warpWarCmds
import time

import servpane
import connpane
import plyrpane
from ConfigHandler import *

class connect(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, cfg):
        self.cfg = cfg
        self.name = StringVar()
        self.name.set(self.cfg.Profile.playerName)
        self.color = StringVar()
        self.color.set(self.cfg.Profile.color)

        self.startBases = StringVar()
        self.startBases.set(self.cfg.Profile.bases) #Someday be a drop downlist

        #  This list must come from the game we connect to
        self.startBaseList = ["Ur Mosul Larsu", "Nineveh Babylon Ugarit"]

        self.client = None
        self.conn = None
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

        self.plyr = plyrpane.plyr(master,self.cfg, borderwidth=1, relief="sunken")
        self.plyr.pack()

        self.serv = servpane.serv(master, borderwidth=1, relief="sunken")
        self.serv.pack()

        self.conn = connpane.conn(master, borderwidth=1, relief="sunken")
        self.conn.pack()

        print("calling use connection   ", self.conn.hCon)
        self.plyr.useConnection(self.conn.hCon)

        return tmp # initial focus

    # PURPOSE:
    # RETURNS:
    def validate(self):
        print("hCon   ", self.conn.hCon)
        print("hConIP   ", self.conn.cfg.Client.serverIP)
        print("hConPort   ", self.conn.cfg.Client.serverPort)
        self.client = self.conn.hCon
        if (self.client is None):
            return False
        return True

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("return the client")
        self.result = self.client
        self.playerName = self.name.get()
        tmp = self.startBases.get()
        self.playerStartBases = tmp.split()
        self.playerColor = self.color.get()
