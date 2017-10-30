#
# Simple scrolling window to display history of game
# Could probably use this for debug
#
from tkinter import *

class history(Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master):
        Frame.__init__(self, master)
        self.text = Text(self, width=30)
        self.text.pack(expand=YES, fill=BOTH)
        self.lastSeqid = 0

    # PURPOSE:
    # RETURNS:
    def set(self, seqid, newText):
        if (seqid > self.lastSeqid):
            self.lastSeqid = seqid
            self.text.insert(INSERT, str(seqid) + ": " + newText)
            print("text", newText)
