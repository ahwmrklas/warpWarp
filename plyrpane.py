# display player information to "join" a game
#
import tkinter as TK

import ConfigHandler
import client
import cmds

class plyr(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, cfg, **kwargs):
        TK.LabelFrame.__init__(self, master, text="Join Game", **kwargs)

        self.hCon = None
        self.cfg  = cfg;
        self.plid = None;

        print("plyrpane --init");
        print("  ", self.cfg.Profile.playerName)
        print("  ", self.cfg.Profile.color)
        print("  ", self.cfg.Profile.bases)
        print("This base list not used")

        #  This list must come from the game we connect to
        self.startBaseList = ["Ur Mosul Larsu", "Nineveh Babylon Ugarit"]

        self.initGui()

        self.useConnection(None, None)

    # PURPOSE: Do all the fun UI things
    # RETURNS: nothing
    def initGui(self):
        self.playerName = TK.Entry(self)
        self.playerName.insert(0, self.cfg.Profile.playerName)
        self.playerName.pack()

        self.playerColor = TK.Entry(self)
        self.playerColor.insert(0, self.cfg.Profile.color)
        self.playerColor.pack()

        self.startBases = TK.StringVar()
        self.startBases.set(self.startBaseList[0])

        self.playerBases = TK.OptionMenu(self, self.startBases, *self.startBaseList)
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
        self.cfg.Profile.bases = self.startBases.get()

        if (self.hCon):
            sendJson = cmds.warpWarCmds().playerLeave(self.cfg.Profile.plid())
            self.hCon.sendCmd(sendJson)

            sendJson = cmds.warpWarCmds().newPlayer(self.cfg.Profile.plid(),
                                                    self.cfg.Profile.playerName,
                                                    self.cfg.Profile.bases.split(" "),
                                                    self.cfg.Profile.color)
            self.hCon.sendCmd(sendJson)

            self.playerName.config(state="disabled")
            self.playerColor.config(state="disabled")
            self.playerBases.config(state="disabled")
            self.config(text="Playing")

            self.joinUnjoin.config(text="Disconnect", command = lambda :self.disconnect())

            self.cfg.saveConfig()

            # record the PlayerID
            self.plid = self.cfg.Profile.plid()

    # PURPOSE: Button handler. The Quit button
    #          call this when "Quit" button clicked
    # RETURNS: I don't know.
    def disconnect(self):
        print("plyr: Disconnection")

        # clear the PlayerID
        slef.plid = None

        self.playerName.config (state="normal")
        self.playerColor.config(state="normal")
        self.playerBases.config(state="normal")
        self.config(text="Join Game")

        self.joinUnjoin.config(text="Join", command = lambda :self.join())

        if (self.hCon):
            sendJson = cmds.warpWarCmds().playerLeave(self.cfg.Profile.plid())
            self.hCon.sendCmd(sendJson)

        print("plyr: stopped playing")

    # PURPOSE: Use the given connection to client to end "join"
    #          update enable/disable nature of widgets
    # RETURNS:
    def useConnection(self, hCon, tmpGame):
        print("plyr: useConnection   ", hCon)
        if (hCon and tmpGame and tmpGame['state']['phase'] == "creating"):
            self.hCon = hCon
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
