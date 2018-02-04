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
        TK.Frame.__init__(self, master, **kwargs)

        print("aipane --init");
        self.hPlayerAi = None

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

        self.aiName = TK.Entry(self)
        self.aiName.insert(0, self.cfg.PlayerAI.name)
        self.aiName.pack()

        # Create a Start button
        self.start = TK.Button(self, text = "Start",
                              command = lambda :self.startAI())
        self.start.pack()

        # Create a quit button (obviously to exit the program)
        self.stop = TK.Button(self, text = "Stop",
                              command = lambda :self.stopAI())
        self.stop.pack()

    # PURPOSE: Start the playerAI thread
    # RETURNS: nothing
    def startAI(self):
        print("aipane: start")
        self.hPlayerAi = playerAi.playerAiThrd(self.aiName.get(),
                                               self.serverEntry.get(),
                                               int(self.portEntry.get())
                                              )

    # PURPOSE: Button handler. The Quit button
    #          Stop the playerAI thresd
    # RETURNS: I don't know.
    def stopAI(self):
        print("aipane: stop the AI")
        if (self.hPlayerAi is not None) :
            self.hPlayerAi.quit()
