# AI Player for WarpWar
#
# This is a brain dead AI. It connects to the
# WarpWar server and holds the place of a player
# and sends and receives messages
#
# Written with Python 3.4.2
#

# Imports
import socket
import threading
from client import comThrd
import queue as Q
import gameserver
from cmds import warpWarCmds

# thread for the player
class playerAiThrd(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self, name, ipAddr, port):
        self.playerName = name
        self.ipAddr = ipAddr
        self.port = port
        self.threadContinue = True
        self.client = None
        threading.Thread.__init__(self, name="playerAiThrd")
        self.start()

    # PURPOSE: For anyone to kill the thread
    # RETURNS: none
    def quit(self):
        print("playerAiThread: quiting")
        self.threadContinue = False

    # PURPOSE: automatically called by base thread class, right?
    #   Waits for clients to send us requests.
    # RETURNS: none
    def run(self):

        tmp = warpWarCmds().ping()
        self.client = comThrd(self.ipAddr, self.port)
        self.client.sendCmd(tmp)
        resp = self.client.waitFor(5)

        print("playerAiRESP:", len(resp))
        if (len(resp) > 0):
            print("playerAiRESP: good len")
        else:
            print("playerAiRESP: bad len")

        self.client.quitCmd()

        print("playerAiThread: socket listen exiting")
