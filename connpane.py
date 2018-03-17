# display connection pane
#
import tkinter as TK
import socket

import ConfigHandler
import client
import cmds

class conn(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, **kwargs):
        TK.LabelFrame.__init__(self, master, text="Not Connected", **kwargs)

        self.cfg = ConfigHandler.ConfigHandler('warpwar.ini')
        print("connpane --init");
        print(self.cfg.Client.serverIP)
        print(self.cfg.Client.serverPort)

        self.conDiscon = None
        self.hCon = None

        self.initGui()

    # PURPOSE: Do all the fun UI things
    # RETURNS: nothing
    def initGui(self):
        self.serverEntry = TK.Entry(self)
        self.serverEntry.insert(0, self.cfg.Client.serverIP)
        self.serverEntry.pack()
        self.portEntry = TK.Entry(self)
        self.portEntry.insert(0, self.cfg.Client.serverPort)
        self.portEntry.pack()

        # Create a button
        self.conDiscon = TK.Button(self, text = "Connect",
                              command = lambda :self.connect())
        self.conDiscon.pack()


    # PURPOSE: Connect to the server
    # RETURNS: nothing
    def connect(self):
        print("conn: Connect")

        self.cfg.Client.serverIP = self.serverEntry.get()
        self.cfg.Client.serverPort = self.portEntry.get()

        self.hCon = client.comThrd(self.cfg.Client.serverIP,
                                   int(self.cfg.Client.serverPort))

        if (self.hCon):
            pingCmd = cmds.warpWarCmds().ping('connectDlg')
            self.hCon.sendCmd(pingCmd)
            resp = self.hCon.waitFor(5)
        else:
            resp = ""

        if (len(resp) > 0):
            print("Connection success!", len(resp))
            self.serverEntry.config(state="disabled")
            self.portEntry.config(state="disabled")
            self.config(text="Connected")

            self.conDiscon.config(text="Disconnect", command = lambda :self.disconnect())

            self.cfg.saveConfig()
        else:
            print("Connection failed:", len(resp))
            self.config(text="Connection Failed")

    # PURPOSE: Button handler. The Quit button
    #          call this when "Quit" button clicked
    # RETURNS: I don't know.
    def disconnect(self):
        print("conn: Disconnection")

        self.serverEntry.config(state="normal")
        self.portEntry.config(state="normal")
        self.config(text="Not Connected")

        self.conDiscon.config(text="Connect", command = lambda :self.connect())

        if (self.hCon is not None) :
            self.hCon.quitCmd()

        self.hCon = None
        print("conn: Client disconnected")
