#
# Demo program to show how to connect to WarpWar server
#

import sys
sys.path.append("/home/ahw/views/warpWar/test")

import socket         # Import socket module
import threading
import queue as Q
import time

# Socket thread
class comThrd(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self, ip, port):
        self.Q = Q.Queue()
        self.hGUI = Q.Queue()
        self.ip = ip
        self.port = port
        threading.Thread.__init__(self, name="ClientComThrd")
        self.start()

    # PURPOSE: For external parties to send a "text" message
    #    send a msg via our Q for our thread to handle
    # RETURNS: none
    def sendCmd(self, msg):
        self.Q.put("send")
        self.Q.put(msg)

    # PURPOSE: For external parties to send a "quit" message
    #    send a msg via our Q for our thread to handle
    # RETURNS: none
    def quitCmd(self):
        self.Q.put("quit")

    # PURPOSE: Get items from the Q
    # RETURNS: return a string
    def pull(self):
        if (not self.hGUI.empty()):
            return self.hGUI.get()
        return None

    # PURPOSE: wait for a response in Q
    # RETURNS: return a string
    def waitFor(self, count):
        resp = self.pull()
        tooMany = count
        while (resp is None):
            if (tooMany <= 0):
                print("Failed to connect")
                return ""
            tooMany -= 1
            resp = self.pull()
            print("sleeping")
            time.sleep(2)

        print("RESP:", len(resp))
        return resp


    # PURPOSE: Our Q holds a message to send to the server. Do so.
    #    Send a message and wait for a response
    # RETURNS: none
    def handleSend(self):
        msg = self.Q.get()
        returnMe = None
        print("client ", self.ip, self.port, msg, "\n")
        try:
            s = socket.socket()
            s.connect((self.ip, self.port))
            s.send(msg.encode())
            cmd = s.recv(4096)
            xmlStr = cmd.decode()
            print("client received (", len(xmlStr), "):\n")
            # print(xmlStr)
            self.hGUI.put(xmlStr)
        except Exception as error:
            returnMe = error
            print("Socket error: ", error, "\n")

        s.close()
        return returnMe

    # PURPOSE: Do what is needed when server sends us a quit message
    # RETURNS: none
    def handleQuit(self):
        print("comThrd-quit command")

    # PURPOSE: automatically called by base thread class, right?
    # RETURNS: none
    def run(self):
        while True:
            cmd = self.Q.get()
            if cmd == "send":
                self.handleSend()
            elif cmd == "quit":
                self.handleQuit()
                break

        print("client comThrd exiting")
