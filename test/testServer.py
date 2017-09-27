# Server for testing warp war. Has no gui
#
# Gui Test driver for Server thread
#

# Imports
# server thread for sending data to and fro
from server import srvrThrd
from playerAi import playerAiThrd
import socket
import threading
import queue as Q
import getpass
import time
# GUI thread for management
class ServerTestApp(threading.Thread):
    
    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        self.Q = Q.Queue()
        self.hNET = None
        self.hPlayerAi = None
        threading.Thread.__init__(self, name="ServerMyTkApp")
        self.start()
        
    # PURPOSE: Button handler. The Quit button
    #          call this when "Quit" button clicked
    # RETURNS: I don't know.
    def quit(self):
        print("STest: quiting?")
        if (self.hPlayerAi is not None) :
            self.hPlayerAi.quit()
            time.sleep(2)
        if (self.hNET is not None) :
            self.hNET.quit()
        print("STest: Server Gui exit")

    # PURPOSE: Start the network server thread
    # RETURNS: nothing
    def startServer(self):
        print("STest: start server")
        self.hNET = srvrThrd(self.host, int(self.port), self)

    # PURPOSE: Start the AI Player
    # RETURNS: nothing
    def startAI(self):
        print("STest: start AI")
        self.hPlayerAi = playerAiThrd(self.player2Name,
                                      self.host,
                                      int(self.port))


    def initValues(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = "12345"
        # Who am I? Pick the other guy
        myName = getpass.getuser()
        if (myName == "ahw"):
            yourName = "bearda"
        else:
            yourName = "ahw"
        self.player2Name = yourName

    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket server uses this
    # RETURNS: none
    def displayAddr(self, msg):
        pass
        
    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket server uses this
    # RETURNS: none
    def displayMsg(self, msg):
        pass

    # PURPOSE: Display data from my GUI Q in box
    # RETURNS: none
    def handleDisplayAddr(self):
        addr = self.Q.get()
        self.recvFrom.set(addr)
        
    # PURPOSE: Display data from my GUI Q in box
    # RETURNS: none
    def handleDisplayMsg(self):
        msg = self.Q.get()
        self.recvMsg.set(msg)
        
    
    # PURPOSE: automatically called by base thread class, right?
    #     create the GUI, wait for msgs on a timer, run the tkinter
    #     thing so the GUI responds to the user
    # RETURNS: none
    def run(self):
        self.initValues()
        self.startServer()
        #self.startAI()
        print("STest: POLL is done?")
        #self.root.mainloop()


# PURPOSE: start up stuff...
# RETURNS: none?
def main():
    hGui = ServerTestApp()
    print("STest: two threads created. Main program exiting")

# Start the main function
if __name__ == "__main__":
   main()

