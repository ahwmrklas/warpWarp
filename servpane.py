# display server information
#
import tkinter as TK
import socket

import ConfigHandler
import server

class serv(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, **kwargs):
        TK.LabelFrame.__init__(self, master, text="Server", **kwargs)

        self.cfg = ConfigHandler.ConfigHandler('warpwar.ini')
        print("serv --init");
        print(self.cfg.Server.serverIP)
        print(self.cfg.Server.serverPort)

        self.startstop = None
        self.hNET = None

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

        # Create a button
        self.startstop = TK.Button(self, text = "Start",
                              command = lambda :self.startServer())
        self.startstop.pack()


    # PURPOSE: Start the network server thread
    # RETURNS: nothing
    def startServer(self):
        print("serv: start server")

        self.cfg.Server.serverIP = self.serverEntry.get()
        self.cfg.Server.serverPort = self.portEntry.get()
        self.cfg.saveConfig()
        self.hNET = server.srvrThrd(self.cfg.Server.serverIP,
                                    int(self.cfg.Server.serverPort),
                                    self)
        print("serv: hNet continue", self.hNET.serverContinue )
        if (self.hNET.serverContinue):
            self.serverEntry.config(state="disabled")
            self.portEntry.config(state="disabled")
            self.config(text="Server Running")
            self.startstop.config(text="Stop", command = lambda :self.quitCB())

    # PURPOSE: Button handler. The Quit button
    #          call this when "Quit" button clicked
    # RETURNS: I don't know.
    def quitCB(self):
        print("serv: quiting?")

        self.serverEntry.config(state="normal")
        self.portEntry.config(state="normal")
        self.config(text="Server")

        self.startstop.config(text="Start", command = lambda :self.startServer())

        if (self.hNET is not None) :
            self.hNET.quit()
        print("serv: Server Gui exit")

    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket server uses this
    #          This is for debug
    #          I can display what the server is doing
    # RETURNS: none
    def displayAddr(self, msg):
        pass
        
    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket server uses this
    # RETURNS: none
    def displayMsg(self, msg):
        pass
