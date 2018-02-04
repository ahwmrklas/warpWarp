#
# Simple scrolling window to display history of game
# Could probably use this for debug
#
import tkinter as TK

class history(TK.Frame):

    # PURPOSE:
    # RETURNS:
    def __init__(self, master, **kwargs):
        TK.Frame.__init__(self, master, **kwargs)
        self.text = TK.Text(self, width=30, state=TK.DISABLED)
        self.text.pack(expand=TK.YES, fill=TK.BOTH)
        self.lastSeqid = 0

    # PURPOSE:
    # RETURNS:
    def set(self, seqid, newText):
        if (seqid > self.lastSeqid):
            self.lastSeqid = seqid
            self.text.config(state=TK.NORMAL)
            self.text.insert(TK.END, str(seqid) + ": " + newText)
            self.text.config(state=TK.DISABLED)
            print("text", newText)
