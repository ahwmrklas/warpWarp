# display Game information to create a game on a server
#
import tkinter as TK

import client
from cmds import warpWarCmds

class gamePane(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, owner, **kwargs):
        TK.LabelFrame.__init__(self, master, text="Game Options", **kwargs)

        self.hCon = None
        self.plid = None
        self.owner = owner
        self.newGameName = "newGame"

        print("gamePane --init");
        self.initGui()
        self.useConnection(None)

    # PURPOSE: Do all the fun UI things
    # RETURNS: nothing
    def initGui(self):
        self.gameName = TK.Entry(self)
        self.gameName.insert(0, self.newGameName)
        self.gameName.pack()

        # Here we need all the options for a game... Size and start bases ....
        # But I don't want to mess with that. I just want the default game created

        self.createBtn = TK.Button(self, text = "CreateGame",
                                    command = lambda :self.create())
        self.createBtn.pack()

    # PURPOSE: Create a game on the server
    # RETURNS: nothing
    def create(self):
        print("gameCreate")

        if (self.hCon):
            sendJson = warpWarCmds().newGame(self.plid,
                                             "dummy",
                                             self.gameName.get())
            self.hCon.sendCmd(sendJson)

            self.gameName.config(state="disabled")
            self.config(text="Playing")
            self.owner.change()

    # PURPOSE: Use the given connection to client to end "join"
    #          update enable/disable nature of widgets
    # RETURNS:
    def useConnection(self, hCon):
        print("gamepane: useConnection   ", hCon)
        if (hCon):
            self.hCon = hCon
            self.createBtn.config(state="normal")
            if (self.createBtn.cget("text") == "Join"):
                self.gameName.config(state="normal")
            else:
                self.gameName.config(state="disabled")
        else:
            self.createBtn.config(state="disabled")
            self.gameName.config(state="disabled")
