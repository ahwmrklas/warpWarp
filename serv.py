# display server information
#
import tkinter as TK
import ConfigHandler

class serv(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master):
        TK.Frame.__init__(self, master)

        self.cfg = ConfigHandler.ConfigHandler('warpwar.ini')
        print("serv --init");
        print(self.cfg.Server.serverIP)
        print(self.cfg.Server.serverPort)
        print(self.cfg.PlayerAI.name)

        self.serverEntry = TK.Entry(self)
        self.serverEntry.insert(0, self.cfg.Server.serverIP)
        self.serverEntry.pack()
        self.portEntry = TK.Entry(self)
        self.portEntry.insert(0, self.cfg.Server.serverPort)
        self.portEntry.pack()
        self.playerAiEntry = TK.Entry(self)
        self.playerAiEntry.insert(0, self.cfg.PlayerAI.name)
        self.playerAiEntry.pack()

        # Create a Start button
        self.start = TK.Button(self, text = "Start",
                              command = lambda :self.startServer())
        self.start.pack()

        # Create a quit button (obviously to exit the program)
        self.quit = TK.Button(self, text = "Quit",
                              command = lambda :self.quitCB())
        self.quit.pack()


    # PURPOSE:
    # RETURNS:
    def set(self, seqid, newText):
        if (seqid > self.lastSeqid):
            self.lastSeqid = seqid
            self.text.config(state=TK.NORMAL)
            self.text.insert(TK.END, str(seqid) + ": " + newText)
            self.text.config(state=TK.DISABLED)
            print("text", newText)
