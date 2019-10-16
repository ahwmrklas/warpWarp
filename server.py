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
import gameserver
import zlib
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
        self.s = None

        try:
            self.s = socket.socket()
            self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.s.bind((self.ipAddr, self.port))

            self.s.listen(5)
        except:
            print("server: Failed to create server at ", self.ipAddr)
            self.serverContinue = False

        threading.Thread.__init__(self, name="ServerSvrThread")
        self.start()

    # PURPOSE: For anyone to kill the thread
    # RETURNS: none
    def quit(self):
        print("server: Sending quit msg to server")
        try:
            tmpS = socket.socket()
            tmpS.connect( (self.ipAddr, self.port) )
            tmp = warpWarCmds()
            sendJson = tmp.quitGame('STest')

            tmpS.send(zlib.compress(sendJson.encode()))
            tmpS.shutdown(socket.SHUT_RDWR)
            tmpS.close()
            tmpS = None
        except Exception as error:
            print("server.py Socket error: ", error, "\n")


    # PURPOSE: automatically called by base thread class, right?
    #   Waits for clients to send us requests.
    # RETURNS: none
    def run(self):

        while self.serverContinue:
           c, addr = self.s.accept()

           compressed = c.recv(8192)
           cmd = zlib.decompress(compressed)
           #print("Rcvd:", cmd.decode())
           self.hGUI.displayAddr(addr)
           self.hGUI.displayMsg(cmd.decode())
           self.gameserver.parseCmd(cmd.decode())
           self.serverContinue = self.gameserver.gameOn()

           # Send client the state of the game
           string = self.gameserver.gameJson().encode()
           compressed = zlib.compress(string)
           c.send(compressed)
           c.close()

        if (self.s):
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            self.s = None

        print("server.py: thread exiting")
