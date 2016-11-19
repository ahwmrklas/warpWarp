#
# Demo program to show how to connect to WarpWar server
#

import sys
sys.path.append("/home/ahw/views/warpWar/test")

import socket         # Import socket module
import threading
import queue as Q

import XML2Py
import Py2XML


# Socket thread
class comThrd(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self, hGui):
        self.Q = Q.Queue()
        self.hGUI = hGui
        threading.Thread.__init__(self, name="ClientComThrd")
        self.start()

    # PURPOSE: For external parties to send a "text" message
    #    send a msg via our Q for our thread to handle
    # RETURNS: none
    def sendCmd(self, ip, port, msg):
        self.Q.put("send")
        self.Q.put(ip)
        self.Q.put(port)
        self.Q.put(msg)

    # PURPOSE: For external parties to send a "quit" message
    #    send a msg via our Q for our thread to handle
    # RETURNS: none
    def quitCmd(self):
        self.Q.put("quit")
        
    # PURPOSE: Our Q holds a message to send to the server. Do so.
    #    Send a message and wait for a response
    # RETURNS: none
    def handleSend(self):
        ip = self.Q.get()
        port = self.Q.get()
        msg = self.Q.get()
        returnMe = None
        print("client ", ip, port, msg, "\n")
        try:
            s = socket.socket()
            s.connect((ip, port))
            s.send(msg.encode())
            cmd = s.recv(4096)
            xmlStr = cmd.decode()
            print("client received (", len(xmlStr), "):\n")
            # print(xmlStr)
            self.hGUI.displayCmd(cmd)
        except Exception as error:
            returnMe = error
            print("Sockect error: ", error, "\n")

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
