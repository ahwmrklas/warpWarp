#
# Demo program to show how to connect to WarpWar server
# This is a test GUI to drive the client and server communications
#

from client import comThrd
from cmds import warpWarCmds

import socket         # Import socket module
import tkinter as tk
import threading
import queue as Q

# GUI thread. This is only for test. The real GUI is the players UI
class myWindow(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        self.Q = Q.Queue()        
        self.hCOM = comThrd(self)
        threading.Thread.__init__(self, name="ClientMyWindow")
        self.start()

    # PURPOSE: Called back for quit. Clean up socket and self
    # RETURNS: none
    def quitCB(self):
        self.hCOM.quitCmd()
        self.root.quit()
        print("Client Gui exit")

    # PURPOSE: Send data via the client socket thread
    # RETURNS: none
    def sendMsg(self):
        # print(self.ip, self.port, self.msg)
        self.hCOM.sendCmd(self.ip.get(), int(self.port.get()), self.msg.get())

    # PURPOSE: Send the new game command
    # RETURNS: none
    def newGame(self):
        # print(self.ip, self.port, self.msg)
        tmp = warpWarCmds()
        sendXml = tmp.newGame("foo")
        print(" client sending: ", sendXml)
        self.hCOM.sendCmd(self.ip.get(), int(self.port.get()), sendXml)
       
       
    # PURPOSE: Construct all the GUI junk
    # RETURNS: nothing
    def initGui(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.protocol("WM_DELETE_WINDOW", self.quitCB)

        tmp = tk.Label(self.root, text="Client: ")
        tmp.grid(row=1, column=0)

        host = socket.gethostname()
        tmp = tk.Label(self.root, text=host)
        tmp.grid(row=1, column=1)

        tmp = tk.Label(self.root, text="Send IP: ")
        tmp.grid(row=2, column=0)
        
        self.ip = tk.StringVar()
        self.ip.set(host)
        self.ipEntry = tk.Entry(self.root, textvariable=self.ip)
        self.ipEntry.grid(row=2, column=1)

        tmp = tk.Label(self.root, text="Send Port: ")
        tmp.grid(row=3, column=0)

        self.port = tk.StringVar()
        self.port.set('12345')
        self.portEntry = tk.Entry(self.root, textvariable=self.port)
        self.portEntry.grid(row=3, column=1)

        tmp = tk.Label(self.root, text="Send Msg: ")
        tmp.grid(row=4, column=0)

        self.msg = tk.StringVar()
        self.msg.set("hi")
        self.msgEntry = tk.Entry(self.root, textvariable=self.msg)
        self.msgEntry.grid(row=4, column=1)

        tmp = tk.Button(self.root, text="Send", command=self.sendMsg)
        tmp.grid(row=5, column=1)

        tmp = tk.Button(self.root, text="newgame", command=self.newGame)
        tmp.grid(row=5, column=2)

        tmp = tk.Label(self.root, text="Resp Msg: ")
        tmp.grid(row=7, column=0)

        self.resp = tk.StringVar()
        self.resp.set("")
        self.respEntry = tk.Entry(self.root, textvariable=self.resp)
        self.respEntry.grid(row=7, column=1)    

    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket client uses this
    # RETURNS: none
    def displayCmd(self, msg):
        self.Q.put(msg)

    # PURPOSE: drain the Q
    #    While this returns. It also starts a timer
    #    that will call this function again
    # RETURNS: none
    def poll(self):
        while not self.Q.empty():
            self.resp.set(self.Q.get())
        self.root.after(2000, self.poll)

    # PURPOSE: automatically called by base thread class, right?
    #     create the GUI, wait for msgs on a timer, run the tkinter
    #     thing so the GUI responds to the user
    # RETURNS: none
    def run(self):
        self.initGui()
        self.poll()
        self.root.mainloop()

# PURPOSE: start up stuff...
# RETURNS: none?
def main():
    lDLG = myWindow()
    print("client: threads created main program exit")


# Start the main function
if __name__ == "__main__":
   main()
