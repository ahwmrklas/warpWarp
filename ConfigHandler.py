from tkinter import *
import configparser
import getpass
import time
import os

from uuid import getnode as get_mac

# Configuration data is stored in an "ini" file
# provide a class to expose that data as properties of The class.
#

class ConfigHandler():

    # Sub sections of the ini file are in sub classes
    # Give default values in the class init functions
    # Which will be overridden by reading the ini file
    class Profile():
        def __init__(self):
            self.playerName = getpass.getuser()
            self.names = []
            self.plids = []
        def squashnames(self):
            return ','.join(self.names)
        def expandnames(self, csv):
            self.names = csv.split(",")
        def squashplids(self):
            return ','.join(self.plids)
        def expandplids(self, csv):
            self.plids = csv.split(",")

        # return the plid for the given player
        #
        def plid(self):
            if (self.playerName not in self.names):
                newplid = str(get_mac()) + str(int(time.time()))
                self.names.append(self.playerName)
                self.plids.append(newplid)

            if (self.playerName in self.names):
                i = self.names.index(self.playerName)
                return self.plids[i]
            else:
                return "Missing plid for "

    class Client():
        def __init__(self):
            self.serverIP = "localhost"
            self.serverPort = 12345
    class Server():
        def __init__(self):
            self.serverIP = "localhost"
            self.serverPort = 12345
    class PlayerAI():
        def __init__(self):
            self.name = "PlayerAI"

    # Set initial values then load the config file to override
    # them (if present)
    def __init__(self, filename):
        self.filename = filename
        self.Profile  = ConfigHandler.Profile()
        self.Client   = ConfigHandler.Client()
        self.Server   = ConfigHandler.Server()
        self.PlayerAI = ConfigHandler.PlayerAI()
        if (os.path.isfile(filename)):
            self.loadConfig()

    # override properties from 'ini' file
    def loadConfig(self):
        print("loadConfig")
        #so we need to open a file select menu, filtering for .wwp
        #and then we load our options
        if (self.filename):
            cfgParser = configparser.ConfigParser()
            cfgParser.read(self.filename)

            if cfgParser.has_option('profile', 'name'):
                self.Profile.playerName = cfgParser.get('profile', 'name')
            if cfgParser.has_option('profile', 'names'):
                self.Profile.expandnames(cfgParser.get('profile', 'names'))
            if cfgParser.has_option('profile', 'plids'):
                self.Profile.expandplids(cfgParser.get('profile', 'plids'))

            if cfgParser.has_option('client', 'serverIP'):
                self.Client.serverIP = cfgParser.get('client', 'serverIP')
            if cfgParser.has_option('client', 'serverPort'):
                self.Client.serverPort = int(cfgParser.get('client', 'serverPort'))

            if cfgParser.has_option('server', 'serverIP'):
                self.Server.serverIP = cfgParser.get('server', 'serverIP')
            if cfgParser.has_option('server', 'serverPort'):
                    self.Server.serverPort = int(cfgParser.get('server', 'serverPort'))

            if cfgParser.has_option('playerai', 'name'):
                self.PlayerAI.name = cfgParser.get('playerai', 'name')

            #we are done here.
        else:
            pass
            #if we get here, we messed up

    # Write properties to 'ini' file
    def saveConfig(self):

        # Make certain the names/plids list is up-to-date
        self.Profile.plid()

        cfgParser = configparser.ConfigParser()
        cfgParser['profile'] = {'name' : self.Profile.playerName,
                                'names' : self.Profile.squashnames(),
                                'plids' : self.Profile.squashplids()}
        cfgParser['client']  = {'serverIP' : self.Client.serverIP,
                                'serverPort' : self.Client.serverPort}
        cfgParser['server']  = {'serverIP' : self.Server.serverIP,
                                'serverPort' : self.Server.serverPort}
        cfgParser['playerai'] = {'name' : self.PlayerAI.name}
        if (self.filename):
            with open(self.filename, 'w') as saveFile:
                cfgParser.write(saveFile)
        else:
            pass
            #if we get here, we messed up.

