#The purpose of this class is to display information on a hex
#The main game should update this when the user hovers over a hex

from tkinter import *

class hexpane(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, text="X=%d, Y=%d" %(0,0), height=10)
        self.label.pack()

    def update(self, objs):
        self.label.destroy()
        _text = ""
        for obj in objs:
            if _text:
                _text += "\n"
            _text += obj['type'] + ":" + obj['name']
        self.label = Label(self, text=_text, height=10, justify="left")
        self.label.pack()

    def shipInfo(ship):
        if (ship['WG']['max']):
            text  =  "Warp" + ship['type']
            if (not ship['WG']['cur']):
                text  +=  "(Drive Currently Damaged)"
        else:
            text  =  "System" + ship['type']

        text = "techLevel " + str(ship['techLevel']) + "\n"
        text +=  "Moves left: " + str(ship['moves']['cur']) + "\n"
        text +=  "PowerDrive: " +  str(ship['PD']['cur']) + "(" + str(ship['PD']['max']) + ")"
        text +=  ", "
        text +=  "Shields " +  str(ship['S']['cur']) + "(" + str(ship['S']['max']) + ")" + "\n"
        text +=  "SystemRacks: " +  str(ship['SR']['cur']) + "(" + str(ship['SR']['max']) + ")"
        text +=  ", "
        text +=  "Beams: " +  str(ship['B']['cur']) + "(" + str(ship['B']['max']) + ")" + "\n"
        text +=  "Tubes: " +  str(ship['T']['cur']) + "(" + str(ship['T']['max']) + ")"
        text +=  " - "
        text +=  "Missiles: " +  str(ship['M']['cur']) + "(" + str(ship['M']['max']) + ")"
        return text



