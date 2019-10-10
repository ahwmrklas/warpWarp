#
# Demo program to show how to connect to WarpWar server
#

import sys
sys.path.append("/home/ahw/views/warpWar/test")

import socket         # Import socket module
import threading
import queue as Q
import time
import zlib


# Socket thread
class comThrd(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self, ip, port):
        self.sendQ = Q.Queue()
        self.rcvQ = Q.Queue()
        self.ip = ip
        self.port = port
        self.callbackWithData = self.defaultCB
        threading.Thread.__init__(self, name="ClientComThrd")
        self.start()

    # PURPOSE: Set the callback function which will be called
    # when we get data from the other end of the socket
    # RETURNS: none
    def setCallback(self, callback):
        self.callbackWithData = callback

    # PURPOSE: For external parties to send a "text" message
    #    send a msg via our Q for our thread to handle
    # RETURNS: none
    def sendCmd(self, msg):
        self.sendQ.put("send")
        self.sendQ.put(msg)

    # PURPOSE: For external parties to send a "quit" message
    #    send a msg via our Q for our thread to handle
    # RETURNS: none
    def quitCmd(self):
        self.sendQ.put("quit")

    # PURPOSE: Default callback. Put data in internal Q
    # RETURNS: return nothing
    def defaultCB(self, data):
        jsonStr = data.decode()
        # print("client received (", len(jsonStr), "):\n")
        # print(jsonStr)
        self.rcvQ.put(jsonStr)

    # PURPOSE: wait for a response in Q
    # RETURNS: return a string
    def waitFor(self, count):
        try:
            resp = self.rcvQ.get(True, count)
        except Q.Empty:
            resp = "{}"
            print("client:Failed waiting for message")

        # print("RESP:", len(resp))
        return resp


    # PURPOSE: Our Q holds a message to send to the server. Do so.
    #    Send a message and wait for a response
    # RETURNS: none
    def handleSend(self):
        msg = self.sendQ.get()
        returnMe = None
        # print("client ", self.ip, self.port, msg, "\n")
        try:
            s = socket.socket()
            s.connect((self.ip, self.port))
            compressed = zlib.compress(msg.encode())
            s.send(compressed)
            time.sleep(0.1)#TODO: fix hack
            compressed = s.recv(8192)
            cmd = zlib.decompress(compressed)
            self.callbackWithData(cmd)
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
            cmd = self.sendQ.get()
            if cmd == "send":
                self.handleSend()
            elif cmd == "quit":
                self.handleQuit()
                break

        print("client comThrd exiting")
