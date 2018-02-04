# Handle the AI Player pane
#
import tkinter as TK
import playerAi

import socket

import ConfigHandler

class aipane(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, **kwargs):
        TK.LabelFrame.__init__(self, master, text="Computer Player", **kwargs)

        print("aipane --init");
        self.hPlayerAi = None
        self.startstop = None

        self.cfg = ConfigHandler.ConfigHandler('warpwar.ini')
        print(self.cfg.PlayerAI.name)
        print(self.cfg.Server.serverIP)
        print(self.cfg.Server.serverPort)

        self.initGui()

    # PURPOSE: Do all the fun UI things
    # RETURNS: nothing
    def initGui(self):
        self.serverEntry = TK.Entry(self)
        self.serverEntry.insert(0, self.cfg.Server.serverIP)
        self.serverEntry.pack()

        self.portEntry = TK.Entry(self)
        self.portEntry.insert(0, self.cfg.Server.serverPort)
        self.portEntry.pack()

        self.aiNameEntry = TK.Entry(self)
        self.aiNameEntry.insert(0, self.cfg.PlayerAI.name)
        self.aiNameEntry.pack()

        # Create a Start button
        self.startstop = TK.Button(self, text = "Start",
                              command = lambda :self.startAI())
        self.startstop.pack()

    # PURPOSE: Start the playerAI thread
    # RETURNS: nothing
    def startAI(self):
        print("aipane: start")

        self.serverEntry.config(state="disabled")
        self.portEntry.config(state="disabled")
        self.aiNameEntry.config(state="disabled")

        self.startstop.config(text="Stop", command = lambda :self.stopAI())

        self.hPlayerAi = playerAi.playerAiThrd(self.aiNameEntry.get(),
                                               self.serverEntry.get(),
                                               int(self.portEntry.get())
                                              )

    # PURPOSE: Button handler. The Quit button
    #          Stop the playerAI thresd
    # RETURNS: I don't know.
    def stopAI(self):
        print("aipane: stop the AI")

        self.serverEntry.config(state="normal")
        self.portEntry.config(state="normal")
        self.aiNameEntry.config(state="normal")

        self.startstop.config(text="Start", command = lambda :self.startAI())

        if (self.hPlayerAi is not None) :
            self.hPlayerAi.quit()
