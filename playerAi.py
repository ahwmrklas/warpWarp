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
import queue as Q
import gameserver
import json
import time
import dataModel
import math
from cmds import warpWarCmds
from client import comThrd

# thread for the player
class playerAiThrd(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self, name, ipAddr, port):
        self.playerName = name
        self.plid = 123
        self.nameCnt = 0
        self.startingBases = ['Babylon', 'Nineveh', 'Ugarit']
        self.color = 'Green'
        self.ipAddr = ipAddr
        self.port = port
        self.threadContinue = True
        self.client = None
        threading.Thread.__init__(self, name="playerAiThrd")
        self.start()

    # PURPOSE: For anyone to kill the thread
    #   called by external parties
    # RETURNS: none
    def quit(self):
        print("playerAi: quiting")
        self.threadContinue = False

    # PURPOSE: Simple ping to the server to read game state
    # RETURNS: game object
    def ping(self):
        sendJson = warpWarCmds().ping(self.plid)
        self.hCon.sendCmd(sendJson)
        resp = self.hCon.waitFor(5)
        game = json.loads(resp)
        return game

    # PURPOSE: 
    # RETURNS: game object
    def newPlayer(self):
        print("playerAi: newPlayer")
        sendJson = warpWarCmds().newPlayer(self.plid,
                                           self.playerName,
                                           self.startingBases,
                                           self.color)
        self.hCon.sendCmd(sendJson)
        resp = self.hCon.waitFor(5)
        game = json.loads(resp)
        self.plid = game['playerList'][-1]['plid']
        print("playerAi:RESP:", len(resp), "plid", self.plid)
        return game

    # PURPOSE: 
    # RETURNS: game object
    def ready(self):
        print("playerAi: ready")
        sendJson = warpWarCmds().ready(self.plid)
        self.hCon.sendCmd(sendJson)
        resp = self.hCon.waitFor(5)
        game = json.loads(resp)
        print("playerAi:RESP:", len(resp))
        return game

    # PURPOSE: Build a "random ship"
    #          Doesn't need to be in class
    # RETURNS: none
    def createShip(self, BP, x, y):
        self.nameCnt += 1
        name = "W" + str(self.nameCnt)
        PD = 5
        WG = True
        B = 3
        S = 3
        T = 2
        M = 2
        SR = 0
        H = 0

        moves = math.ceil(int(PD/2))
        ship =  {
             'name': name,
             'type': "ship",
             'location': {'x':x, 'y':y},
             'image':"ship1.png",
             'owner': self.plid,
             'techLevel': 1,
             'damage': 0,
             'moves': {'max': moves, 'cur': moves },
             'PD': {'max': PD, 'cur': PD },       # PowerDrive
             'WG': {'max': WG, 'cur': WG }, # Warp Generator
             'B':  {'max':B, 'cur':B },       # Beams
             'S':  {'max':S, 'cur':S },       # Screens (Shields)
             'E':  {'max':0, 'cur':0 },       # Electronic Counter Measures (New)
             'T':  {'max':T, 'cur':T },       # Tubes
             'M':  {'max':M * 3, 'cur':M * 3 },       # Missiles
             'A':  {'max':0, 'cur':0 },       # Armor (New)
             'C':  {'max':0, 'cur':0 },       # Cannons (New)
             'SH': {'max':0 * 6, 'cur':0 * 6 },       # Shells (New)
             'SR': {'max':SR, 'cur':SR },       # System Ship Racks
             'H':  {'max':H, 'cur':H },       # Holds (New)
             'Hauled':0,
             'R': {'max':0, 'cur':0 },       # Repair Bays (New)
             'visibility':[ {'player':self.plid,  'percent':100}],
             'carried_ships' :[],
            }
        return ship

    # PURPOSE: 
    # RETURNS: none
    def moveShip(self, ship, game):
        # Where am I
        curLoc = ship['location']
        # How far can I go
        curRange = ship['moves']['cur']
        # Where *should* I go?
        #   Pick up BP
        #   Drop off BP
        #   Conquer planet
        #   Attack enemy ship
        #   Pick up System Ship
        #   Drop off System Ship
        # I'd like to create a random objective and store it with
        # The ship. For now just conquer and attack.

        # Find the nearest thing that I don't own.

    # PURPOSE: 
    # RETURNS: none
    def selectDamageShip(self, ship):
        assert(ship)

        damLeft = ship['damage']
        print("playerAi:", ship['name'], " taking ", damLeft, " damage ")

        # Drain Holds and System Racks
        changeCheck = 0
        while ((damLeft > 0) and damLeft != changeCheck):
            changeCheck = damLeft
            if (damLeft > 0):
                if (ship['H']['cur'] > 0):
                    ship['H']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['SR']['cur'] > 0):
                    ship['SR']['cur'] -= 1
                    damLeft -= 1

        changeCheck = 0
        while ((damLeft > 0) and damLeft != changeCheck):
            changeCheck = damLeft
            if (damLeft > 0):
                if (ship['T']['cur'] > 2):
                    ship['T']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['S']['cur'] > 2):
                    ship['S']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['B']['cur'] > 2):
                    ship['B']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['PD']['cur'] > 4):
                    ship['PD']['cur'] -= 1
                    damLeft -= 1

        changeCheck = 0
        while ((damLeft > 0) and damLeft != changeCheck):
            changeCheck = damLeft
            if (damLeft > 0):
                if (ship['T']['cur'] > 1):
                    ship['T']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['S']['cur'] > 1):
                    ship['S']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['B']['cur'] > 1):
                    ship['B']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['PD']['cur'] > 2):
                    ship['PD']['cur'] -= 1
                    damLeft -= 1

        changeCheck = 0
        while ((damLeft > 0) and damLeft != changeCheck):
            changeCheck = damLeft
            if (damLeft > 0):
                if (ship['T']['cur'] > 0):
                    ship['T']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['S']['cur'] > 0):
                    ship['S']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['B']['cur'] > 0):
                    ship['B']['cur'] -= 1
                    damLeft -= 1
            if (damLeft > 0):
                if (ship['PD']['cur'] > 0):
                    ship['PD']['cur'] -= 1
                    damLeft -= 1

        # This better be zero ... or the ship explodes
        ship['damage'] = damLeft

    # PURPOSE: 
    # RETURNS: none
    def buildThings(self, game):
        # Loop through every base I own
        baseList = dataModel.getOwnedListOfType(game, self.plid, 'starBaseList')
        for base in baseList:
            # Take the points at that base and build a ship there
            print("playerAI: build something at ",
                  base['name'],
                  " for ", base['BP']['cur'])
            ship = self.createShip(base['BP']['cur'], base['location']['x'],
                                                      base['location']['y'])
            if ship:
                sendJson = warpWarCmds().buildShip(self.plid,
                                                   ship,
                                                   base['name'])
                self.hCon.sendCmd(sendJson)
                resp = self.hCon.waitFor(5)
                game = json.loads(resp)

    # PURPOSE: 
    # RETURNS: none
    def moveThings(self, game):
        # Loop through every ship I own
        shipList = dataModel.getOwnedListOfType(game, self.plid, 'shipList')
        for ship in shipList:
            print("playerAI: move ship", ship['name'], " at ",
                   ship['location']['x'], ", ", ship['location']['y'])
            self.moveShip(ship, game)
 


    # PURPOSE: 
    # RETURNS: game object
    def combatOrders(self):
        print("playerAi: combatOrders (nothing right now)")
        #sendJson = warpWarCmds().combatOrders(self.plid, tkRoot.battleOrders)
        #self.hCon.sendCmd(sendJson)
        #resp = self.hCon.waitFor(5)
        #game = json.loads(resp)
        #print("playerAi:RESP:", len(resp))

    # PURPOSE: 
    # RETURNS: none
    def selectDamageAll(self, game):
        print("playerAi: select damage")
        # Find ships with damage
        for ship in game['objects']['shipList']:
            if (ship['owner'] == self.plid) and (ship['damage'] > 0):
                self.selectDamageShip(ship)
                sendJson = warpWarCmds().acceptDamage(self.plid, ship)
                self.hCon.sendCmd(sendJson)
                resp = self.hCon.waitFor(5)
                # I think we can ignore the response

    # PURPOSE: automatically called by base thread class, right?
    #   Waits for clients to send us requests.
    # RETURNS: none
    def run(self):

        gamePhase = None
        playerPhase = None

        self.hCon = comThrd(self.ipAddr, self.port)

        while (self.threadContinue):
            # Ping
            game = self.ping()
            time.sleep(1)

            playerMe = dataModel.playerTableGet(game, self.plid)
            if (playerMe is None):
                playerMe = {'phase':None}

            # What is the current game state and player state?
            if ( (gamePhase == game['state']['phase']) and
                 (playerPhase == playerMe['phase']) ):
                 continue

            gamePhase   = game['state']['phase']
            playerPhase = playerMe['phase']

            # Do something with that state
            print("playerAi:GP ", gamePhase, " PP ", playerPhase)
            if (gamePhase == "creating"):
                if ( (playerPhase is None) or (playerPhase == "nil")):
                    self.newPlayer()
                elif (playerPhase == "creating"):
                    self.ready()
            elif (gamePhase == "build"):
                if (playerPhase == "build"):
                    self.buildThings(game)
                    self.ready()
            elif (gamePhase == "move"):
                if (playerPhase == "move"):
                    self.moveThings(game)
                    self.ready()
            elif (gamePhase == "combat"):
                if (playerPhase == "combat"):
                    self.combatOrders()
                    self.ready()
            elif (gamePhase == "damageselection"):
                if (playerPhase == "damageselection"):
                    self.selectDamageAll(game)
                    self.ready()

        self.hCon.quitCmd()

        print("playerAi:run: exiting")
