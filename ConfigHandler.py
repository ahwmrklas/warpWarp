from tkinter import *
import configparser
import getpass
import time
import os

from uuid import getnode as get_mac

class ConfigHandler():
    def __init__(self, tkRoot):
        self.tkRoot = tkRoot
        if (os.path.isfile("warpwar.ini")):
            self.loadConfig()
        else:
            self.createConfig()


    def loadConfig(self):
        print("loadConfig")
        #so we need to open a file select menu, filtering for .wwp
        #and then we load our options
        loadFileName = "warpwar.ini"
        if (loadFileName):
            configParser = configparser.ConfigParser()
            configParser.read(loadFileName)
            self.tkRoot.playerName = configParser.get('profile', 'name')
            self.tkRoot.plid = int(configParser.get('profile', 'plid'))
            #we are done here.
        else:
            pass
            #if we get here, we messed up

    def createConfig(self):
        self.tkRoot.playerName = getpass.getuser()
        self.tkRoot.plid = int(str(get_mac()) + str(int(time.time())))
        saveFileName = "warpwar.ini"
        configParser = configparser.ConfigParser()
        configParser['profile'] = {'name' : self.tkRoot.playerName,
                                   'plid' : self.tkRoot.plid}
        if (saveFileName):
            with open(saveFileName, 'w') as saveFile:
                configParser.write(saveFile)
        else:
            pass
            #if we get here, we messed up.

