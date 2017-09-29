#The purpose of this class is to make writing unit tests really easy.
#The user should be able to create a server, a client, and connect
#them with one command.

from client import comThrd
from test.testServer import ServerTestApp
import json
import sys
import time
from cmds import warpWarCmds

class UnitTest():
    def __init__ (self, plid=845733184055071504452410,
                    ipAddr="127.0.1.1", port=12345):

        self.plid = plid
        self.server = ServerTestApp()
        self.ipAddr = ipAddr
        self.port = port
        self.hCon = comThrd(self.ipAddr, self.port)
        self.loadedGame = None #game loaded from file
        self.game = None #game received from server
        
        print("Server is live! Wait 1 second and ping")
        time.sleep(1)

        sendJson = warpWarCmds().ping(plid)
        self.hCon.sendCmd(sendJson)
        resp = self.hCon.waitFor(5)

        print("We pinged the server. Remember to Load a game!")

    def loadGame(self, fileName):
        """
        This takes a .wwr file and loads it.

        Note that this DOES NOT send it to the server!
        This is in case the user wants to validate it first.
        """
        loadFile = open(fileName, 'r')
        gameString = loadFile.read()
        loadFile.close()
        self.loadedGame = json.loads(gameString)

    def restoreGame(self):
        """
        This sends the loaded game. I
        Note that this DOES NOT populate self.loadedGame
        """
        sendJson = warpWarCmds().restoreGame(self.plid, self.loadedGame)
        self.hCon.sendCmd(sendJson)
        resp = self.hCon.waitFor(5)
        self.game = json.loads(resp)

    def sendCmd(self, cmd):
        """
        This sends the warpWarCmd you pass it. Not very useful right now
        """
        self.hCon.sendCmd(cmd)
        resp = self.hCon.waitFor(5)
        self.game = json.loads(resp)

    def finishTest(self):
        """
        Kill everything. we are done here
        """

        self.server.quit()
        self.hCon.quitCmd()

