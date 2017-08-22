# All this does is poll the server every second looking for updates.

# Imports
import threading
import json
from time import sleep
from cmds import warpWarCmds

class PollThread(threading.Thread):
    def __init__(self, plid, tkRoot):
        #we must be very careful that we never mess with tkRoot.
        #the only thing we shoudl do is generate an event right before dying
        self.plid = plid
        self.tkRoot = tkRoot
        self.cmdJson = warpWarCmds().poll(self.plid)
        print ("PollThread: initializing")
        threading.Thread.__init__(self, name="pollThread")
        self.start()

    def run(self):
        doneWaiting = 0
        print ("PollThread: starting run")
        while not doneWaiting:
            #poll the server!
            if (self.tkRoot.hCon is not None):
                print("PollThread: main sending: ", self.cmdJson)
                self.tkRoot.hCon.sendCmd(self.cmdJson)
                resp = self.tkRoot.hCon.waitFor(5)
                gameDict = json.loads(resp)
                if gameDict:
                    self.tkRoot.game = json.loads(resp)
                    self.tkRoot.event_generate("<<updateWWMenu>>", when='tail')
                    print ("PollThread: done waiting")
                    doneWaiting = 1
                else:
                    sleep(1)
