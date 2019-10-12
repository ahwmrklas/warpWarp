# Dialog to connect to game server

import tkinter as tk
from tkinter.simpledialog import *
from client import comThrd
from cmds import warpWarCmds
import time

import servpane
import connpane
import plyrpane
import aipane
from ConfigHandler import *

class connect(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, cfg):
        self.cfg = cfg

        self.hCon = None
        self.plid = None
        self.hPlayerAi = None

        Dialog.__init__(self, master)

    # PURPOSE: Callback from child panes when something
    #          changes. Cause other panes to update
    # RETURNS:
    def change(self):
        self.plyr.useConnection(self.conn.hCon)

    # PURPOSE:
    # RETURNS:
    def body(self, master):

        master.pack(fill=BOTH, expand=1)

        self.plyr = plyrpane.plyr(master, self.cfg, borderwidth=1, relief="sunken")
        self.plyr.pack()

        self.ai = aipane.aipane(master, borderwidth=1, relief="sunken")
        self.ai.pack()

        self.serv = servpane.serv(master, borderwidth=1, relief="sunken")
        self.serv.pack()

        self.conn = connpane.conn(master, self, borderwidth=1, relief="sunken")
        self.conn.pack()

        # update the panes with info about each other
        self.change()

        return self.conn  # initial focus

    # PURPOSE:
    # RETURNS:
    def validate(self):
        print("hCon   ", self.conn.hCon)
        print("hConIP   ", self.conn.cfg.Client.serverIP)
        print("hConPort   ", self.conn.cfg.Client.serverPort)
        if (self.conn.hCon is None):
            return False
        return True

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("return the client")

        # Handle for the connection to the server is in the connection pane
        self.hCon = self.conn.hCon

        # PlayerID can be used to look up all player information
        self.plid = self.plyr.plid

        self.hPlayerAi = self.ai.hPlayerAi
