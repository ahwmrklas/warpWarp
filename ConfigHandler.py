from tkinter import *
from tkinter.simpledialog import *
import configparser
import getpass
import time

from uuid import getnode as get_mac

class ConfigHandler(Dialog):
    def __init__(self, tkRoot):
        self.tkRoot = tkRoot
        Dialog.__init__(self, tkRoot)

    def body(self, master):
        #really simple question
        Label(master,text="Create or Load profile?").pack()

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="Load", width=10, command=self.loadConfig, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Create", width=10, command=self.createConfig)
        w.pack(side=LEFT, padx=5, pady=5)
        box.pack()

    def loadConfig(self):
        print("loadConfig")
        #so we need to open a file select menu, filtering for .wwp
        #and then we load our options
        loadFileName = filedialog.askopenfilename(title = "Select file",filetypes = (("warpWar profile","*.wwp"),("all files","*.*")))
        if (loadFileName):
            configParser = configparser.ConfigParser()
            configParser.read(loadFileName)
            self.tkRoot.playerName = configParser.get('profile', 'name')
            self.tkRoot.plid = int(configParser.get('profile', 'plid'))
            #we are done here. kill the window
            self.cancel()
        else:
            pass
            #if we get here, we go back to the parent dialog, no muss, no fuss.

    def createConfig(self):
        self.tkRoot.playerName = getpass.getuser()
        self.tkRoot.plid = str(get_mac()) + str(int(time.time()))
        saveFileName = filedialog.asksaveasfilename(title = "Write your user profile to disk", 
                filetypes = (("warpWar Profile","*.wwp"),("all files","*.*")))
        configParser = configparser.ConfigParser()
        configParser['profile'] = {'name' : self.tkRoot.playerName,
                                   'plid' : self.tkRoot.plid}
        if (saveFileName):
            with open(saveFileName, 'w') as saveFile:
                configParser.write(saveFile)
            self.cancel()
        else:
            pass
            #if we get here, we go back to the parent dialog, no muss, no fuss.

