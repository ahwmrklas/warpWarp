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

    def __init__(self, filename):
        self.filename = filename
        self.Profile = ConfigHandler.Profile()
        self.Client = ConfigHandler.Client()
        self.Server = ConfigHandler.Server()
        if (os.path.isfile(filename)):
            self.loadConfig()

    def loadConfig(self):
        print("loadConfig")
        #so we need to open a file select menu, filtering for .wwp
        #and then we load our options
        loadFileName = self.filename
        if (loadFileName):
            configParser = configparser.ConfigParser()
            configParser.read(loadFileName)
            self.Profile.playerName = configParser.get('profile', 'name')
            self.Profile.plid = int(configParser.get('profile', 'plid'))
            self.Client.serverIP = configParser.get('client', 'serverIP')
            self.Client.serverPort = int(configParser.get('client', 'serverPort'))
            self.Server.serverIP = configParser.get('server', 'serverIP')
            self.Server.serverPort = int(configParser.get('server', 'serverPort'))
            #we are done here.
        else:
            pass
            #if we get here, we messed up

    def saveConfig(self):
        saveFileName = self.filename
        configParser = configparser.ConfigParser()
        configParser['profile'] = {'name' : self.Profile.playerName,
                                   'plid' : self.Profile.plid}
        configParser['client'] = {'serverIP' : self.Client.serverIP,
                                  'serverPort' : self.Client.serverPort}
        configParser['server'] = {'serverIP' : self.Server.serverIP,
                                  'serverPort' : self.Server.serverPort}
        if (saveFileName):
            with open(saveFileName, 'w') as saveFile:
                configParser.write(saveFile)
        else:
            pass
            #if we get here, we messed up.

