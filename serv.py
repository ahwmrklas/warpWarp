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
        TK.Frame.__init__(self, master, **kwargs)

        self.cfg = ConfigHandler.ConfigHandler('warpwar.ini')
        print("serv --init");
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

        # Create a Start button
        self.start = TK.Button(self, text = "Start",
                              command = lambda :self.startServer())
        self.start.pack()

        # Create a quit button (obviously to exit the program)
        self.stop = TK.Button(self, text = "Stop",
                              command = lambda :self.quitCB())
        self.stop.pack()

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

    # PURPOSE: Button handler. The Quit button
    #          call this when "Quit" button clicked
    # RETURNS: I don't know.
    def quitCB(self):
        print("serv: quiting?")
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

    # PURPOSE:
    # RETURNS:
    def set(self, seqid, newText):
        if (seqid > self.lastSeqid):
            self.lastSeqid = seqid
            self.text.config(state=TK.NORMAL)
            self.text.insert(TK.END, str(seqid) + ": " + newText)
            self.text.config(state=TK.DISABLED)
            print("text", newText)
