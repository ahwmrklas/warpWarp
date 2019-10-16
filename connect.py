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
import json
import gamepane
from ConfigHandler import *
from cmds import warpWarCmds

class connect(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, cfg):
        self.cfg = cfg

        self.hCon = None
        self.plid = None
        self.hPlayerAi = None
        self.tmpGame = None

        Dialog.__init__(self, master)

    # PURPOSE:
    # RETURNS:
    def newDataForGame(self, data):
        print("connect.py: newDataForGame ")
        jsonStr = data.decode()
        tmpGame = json.loads(jsonStr)
        self.plyr.useConnection(self.conn.hCon, tmpGame)

    # PURPOSE: Callback from child panes when something
    #          changes. Cause other panes to update
    # RETURNS:
    def change(self):
        print("connect.py: change ")
        self.plyr.useConnection(self.conn.hCon, {})
        self.gp.useConnection(self.conn.hCon)
        if (self.conn.hCon):
            self.conn.hCon.setCallback(lambda data: self.newDataForGame(data))
            sendJson = warpWarCmds().ping(self.plid)
            self.conn.hCon.sendCmd(sendJson)

    # PURPOSE:
    # RETURNS:
    #    self.event_generate("<<myOnChange>>", when='tail')
    def myOnChange(self, event):
        print("myOnChange")

    # PURPOSE:
    # RETURNS:
    def body(self, master):

        self.bind("<<myOnChange>>", lambda event :self.myOnChange(event))

        master.pack(fill=BOTH, expand=1)

        self.plyr = plyrpane.plyr(master, self.cfg, borderwidth=1, relief="sunken")
        self.plyr.pack()

        self.ai = aipane.aipane(master, borderwidth=1, relief="sunken")
        self.ai.pack()

        self.serv = servpane.serv(master, borderwidth=1, relief="sunken")
        self.serv.pack()

        self.gp = gamepane.gamePane(master, self, borderwidth=1, relief="sunken")
        self.gp.pack()

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
