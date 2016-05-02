# Server for WarpWar game
#
# Clients connect to this program and it handles build
# and battle instructions and responds to all parties with the battle
# results and the map results after builds and moves
#
# Written with Python 3.4.2
#

# Imports
import socket
import tkinter as tk
import threading
import queue as Q
import gameserver

# server thread for sending data to and fro
class srvrThrd(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self, ipAddr, port, hGui):
        self.ipAddr = ipAddr
        self.port = port
        self.hGUI = hGui
        self.serverContinue = True
        self.gameserver = gameserver.gameserver()
        threading.Thread.__init__(self)
        self.start()

    # PURPOSE: automatically called by base thread class, right?
    #   Waits for clients to send us requests.
    # RETURNS: none
    def run(self):
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ipAddr, self.port))

        s.listen(5)
        while self.serverContinue:
           c, addr = s.accept()

           cmd = c.recv(1024)
           self.hGUI.displayAddr(addr)
           self.hGUI.displayMsg(cmd.decode())
           self.gameserver.parseCmd(cmd.decode())
           self.serverContinue = self.gameserver.gameOn()

           # Send client the state of the game
           c.send(self.gameserver.gameXml().encode())
           c.close()

        print("socket listen exiting")


# GUI thread for management
class MyTkApp(threading.Thread):
    
    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        self.Q = Q.Queue()
        self.hNET = None
        threading.Thread.__init__(self)
        self.start()
        
    # PURPOSE: Button handler. The Quit button
    #          call this when "Quit" button clicked
    # RETURNS: I don't know.
    def quitCB(self):
        print("quiting?")
        try:
            s = socket.socket()
            s.connect( (self.host.get(), int(self.port.get())) )
            msg = "quit"
            s.send(msg.encode())
            s.close()
        except:
            print("Socket error. Only GUI closes")

        self.root.quit()
        print("Server Gui exit")

    # PURPOSE: Start the network server thread
    # RETURNS: nothing
    def startServer(self):
        print("start server")
        self.hNET = srvrThrd(self.host.get(), int(self.port.get()), self)

    # PURPOSE: Construct all the GUI junk
    # RETURNS: nothing
    def initGui(self):
        self.root = tk.Tk()
        self.root.title("Server IP:port")
        self.root.protocol("WM_DELETE_WINDOW", self.quitCB)

        tmp = tk.Label(self.root, text="Server: ")
        tmp.grid(row=1, column=0)

        host = socket.gethostbyname(socket.gethostname())
        self.host = tk.StringVar()
        self.host.set(host)
        self.serverEntry = tk.Entry(self.root, textvariable=self.host)
        self.serverEntry.grid(row=1, column=1)

        port = '12345'
        self.port = tk.StringVar()
        self.port.set(port)
        self.portEntry = tk.Entry(self.root, textvariable=self.port)
        self.portEntry.grid(row=1, column=2)

        tmp = tk.Label(self.root, text="Send Msg: ")
        tmp.grid(row=3, column=0)
        
        self.sendMsg = tk.StringVar()
        self.sendMsg.set("")
        self.sendMsgEntry = tk.Entry(self.root, textvariable=self.sendMsg)
        self.sendMsgEntry.grid(row=3, column=1)
        
        tmp = tk.Label(self.root, text="Received From: ")
        tmp.grid(row=5, column=0)
        
        self.recvFrom = tk.StringVar()
        self.recvFrom.set("")
        self.recvFromEntry = tk.Entry(self.root, textvariable=self.recvFrom)
        self.recvFromEntry.grid(row=5, column=1)

        tmp = tk.Label(self.root, text="Received Msg: ")
        tmp.grid(row=6, column=0)
        
        self.recvMsg = tk.StringVar()
        self.recvMsg.set("")
        self.recvMsgEntry = tk.Entry(self.root, textvariable=self.recvMsg)
        self.recvMsgEntry.grid(row=6, column=1)

        # Create a Start button
        self.quit = tk.Button(text = "Start",
                              command = lambda :self.startServer())
        self.quit.grid(row=7, column=1)

        # Create a quit button (obviously to exit the program)
        self.quit = tk.Button(text = "Quit",
                              command = lambda :self.quitCB())
        self.quit.grid(row=7, column=2)

    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket server uses this
    # RETURNS: none
    def displayAddr(self, msg):
        self.Q.put("addr")
        self.Q.put(msg)
        
    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket server uses this
    # RETURNS: none
    def displayMsg(self, msg):
        self.Q.put("msg")
        self.Q.put(msg)        

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
        
    # PURPOSE: drain the Q
    #    While this returns. It also starts a timer
    #    that will call this function again
    # RETURNS: none
    def poll(self):

        while not self.Q.empty():
            cmd = self.Q.get()
            if (cmd == "addr"):
                self.handleDisplayAddr()
            elif (cmd == "msg"):
                self.handleDisplayMsg()

        self.root.after(2000, self.poll)
    
    # PURPOSE: automatically called by base thread class, right?
    #     create the GUI, wait for msgs on a timer, run the tkinter
    #     thing so the GUI responds to the user
    # RETURNS: none
    def run(self):
        self.initGui()
        self.poll()
        print("POLL is done?")
        self.root.mainloop()


# PURPOSE: start up stuff...
# RETURNS: none?
def main():
    hGui = MyTkApp()
    print("two threads created. Main program exiting")

# Start the main function
if __name__ == "__main__":
   main()
