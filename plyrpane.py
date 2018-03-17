# display player information to "join" a game
#
import tkinter as TK
import socket

import ConfigHandler
import client
import cmds

class plyr(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, **kwargs):
        TK.LabelFrame.__init__(self, master, text="Join Game", **kwargs)

        self.hCon = None

        self.cfg = ConfigHandler.ConfigHandler('warpwar.ini')
        print("plyrpane --init");
        print(self.cfg.Profile.playerName)
        print(self.cfg.Profile.color)
        print(self.cfg.Profile.bases)

        self.initGui()

    # PURPOSE: Do all the fun UI things
    # RETURNS: nothing
    def initGui(self):
        self.playerName = TK.Entry(self)
        self.playerName.insert(0, self.cfg.Profile.playerName)
        self.playerName.pack()

        self.playerColor = TK.Entry(self)
        self.playerColor.insert(0, self.cfg.Profile.color)
        self.playerColor.pack()

        self.playerBases = TK.Entry(self)
        self.playerBases.insert(0, self.cfg.Profile.bases)
        self.playerBases.pack()

        # Create a button
        self.joinUnjoin = TK.Button(self, text = "Join",
                                    command = lambda :self.join())
        self.joinUnjoin.pack()

    # PURPOSE: Join an existing game on server
    # RETURNS: nothing
    def join(self):
        print("plyr: Join")

        self.cfg.Profile.playerName = self.playerName.get()
        self.cfg.Profile.color = self.playerColor.get()
        self.cfg.Profile.bases = self.playerBases.get()

        if (self.hCon):
            sendJson = cmds.warpWarCmds().removePlayer(self.cfg.Profile.plid())
            self.hCon.sendCmd(sendJson)

            sendJson = cmds.warpWarCmds().newPlayer(self.cfg.Profile.plid(),
                                                    self.cfg.Profile.playerName,
                                                    self.cfg.Profile.bases,
                                                    self.cfg.Profile.color)
            self.hCon.sendCmd(sendJson)

            self.playerName.config(state="disabled")
            self.playerColor.config(state="disabled")
            self.playerBases.config(state="disabled")
            self.config(text="Playing")

            self.joinUnjoin.config(text="Disconnect", command = lambda :self.disconnect())

            self.cfg.saveConfig()

    # PURPOSE: Button handler. The Quit button
    #          call this when "Quit" button clicked
    # RETURNS: I don't know.
    def disconnect(self):
        print("plyr: Disconnection")

        self.playerName.config (state="normal")
        self.playerColor.config(state="normal")
        self.playerBases.config(state="normal")
        self.config(text="Join Game")

        self.joinUnjoin.config(text="Join", command = lambda :self.join())

        if (self.hCon):
            sendJson = cmds.warpWarCmds().removePlayer(self.cfg.Profile.plid())
            self.hCon.sendCmd(sendJson)

        print("plyr: stopped playing")

    # PURPOSE: Use the given connection to client to end "join"
    #          update enable/disable nature of widgets
    # RETURNS:
    def useConnection(self, hCon):
        self.hCon = hCon
        if (self.hCon):
            self.joinUnjoin.config(state="normal")
            if (self.joinUnjoin.cget("text") == "Join"):
                self.playerName.config(state="normal")
                self.playerColor.config(state="normal")
                self.playerBases.config(state="normal")
            else:
                self.playerName.config(state="disabled")
                self.playerColor.config(state="disabled")
                self.playerBases.config(state="disabled")
        else:
            self.joinUnjoin.config(state="disabled")
            self.playerName.config(state="disabled")
            self.playerColor.config(state="disabled")
            self.playerBases.config(state="disabled")
