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
from cmds import warpWarCmds

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
        threading.Thread.__init__(self, name="ServerSvrThread")
        self.start()

    # PURPOSE: For anyone to kill the thread
    # RETURNS: none
    def quit(self):
        print("server: Sending quit msg to server")
        try:
            s = socket.socket()
            s.connect( (self.ipAddr, self.port) )
            tmp = warpWarCmds()
            sendJson = tmp.quitGame()

            s.send(sendJson.encode())
            s.close()
        except:
            print("server: Socket error. Only GUI closes")


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
           #print("Rcvd:", cmd.decode())
           self.hGUI.displayAddr(addr)
           self.hGUI.displayMsg(cmd.decode())
           self.gameserver.parseCmd(cmd.decode())
           self.serverContinue = self.gameserver.gameOn()

           # Send client the state of the game
           c.send(self.gameserver.gameJson().encode())
           c.close()

        print("server: socket listen exiting")
