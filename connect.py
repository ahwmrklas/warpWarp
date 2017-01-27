# Dialog to connect to game server

import tkinter as tk
from tkinter.simpledialog import *
from client import comThrd
from cmds import warpWarCmds
import time

class connect(Dialog):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, defaultIP, defaultPort):
        self.ip = StringVar()
        self.ip.set(defaultIP)
        self.port = IntVar()
        self.port.set(defaultPort)
        self.client = None
        Dialog.__init__(self, master)

    # PURPOSE:
    # RETURNS:
    def body(self, master):

        master.pack(fill=BOTH, expand=1)

        tmp = Label(master, text="SeverIP")
        tmp.pack()

        tmp = tk.Entry(master, textvariable=self.ip)
        tmp.pack()

        tmp = Label(master, text="Port")
        tmp.pack()

        tmp = tk.Entry(master, textvariable=self.port)
        tmp.pack()

        return tmp # initial focus

    # PURPOSE:
    # RETURNS:
    def validate(self):
        print("IP   ", self.ip.get())
        print("PORT ", self.port.get())
        tmp = warpWarCmds().ping()
        self.client = comThrd(self.ip.get(), self.port.get())
        self.client.sendCmd(tmp)
        resp = self.client.waitFor(5)

        print("RESP:", len(resp))
        if (len(resp) > 0):
            return True
        else:
            return False

    # PURPOSE:
    # RETURNS:
    def apply(self):
        print("return the client")
        self.result = self.client
