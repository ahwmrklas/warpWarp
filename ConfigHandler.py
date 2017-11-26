from tkinter import *
import configparser
import getpass
import time
import os

from uuid import getnode as get_mac


class ConfigHandler():
    class Profile():
        def __init__(self):
            self.playerName = getpass.getuser()
            self.plid = int(str(get_mac()) + str(int(time.time())))
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

    def __init__(self, filename):
        self.filename = filename
        self.Profile = ConfigHandler.Profile()
        self.Client = ConfigHandler.Client()
        self.Server = ConfigHandler.Server()
        self.PlayerAI = ConfigHandler.PlayerAI()
        if (os.path.isfile(filename)):
            self.loadConfig()

    def loadConfig(self):
        print("loadConfig")
        #so we need to open a file select menu, filtering for .wwp
        #and then we load our options
        if (self.filename):
            cfgParser = configparser.ConfigParser()
            cfgParser.read(self.filename)

            if cfgParser.has_option('profile', 'name'):
                self.Profile.playerName = cfgParser.get('profile', 'name')
            if cfgParser.has_option('profile', 'plid'):
                self.Profile.plid = int(cfgParser.get('profile', 'plid'))

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

    def saveConfig(self):
        cfgParser = configparser.ConfigParser()
        cfgParser['profile'] = {'name' : self.Profile.playerName,
                                'plid' : self.Profile.plid}
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

