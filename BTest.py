# Demo program to show how to Handle a combat
# Will need a main tk window so the combat dialog and
# Be a child of it?
# This Drives the combat dialog and someday drives
# The various dialogs to make the combat progress.
#

from combat import combat

import tkinter as tk
from samplegame import sampleGame

# PURPOSE:
#  create bare page
# RETURNS: none
def main():
    lists = sampleGame['objects']
    shipList = lists['shipList']

    root = tk.Tk()
    root.title("testCombat")
    combat(root, shipList, [])
    root.mainloop()

# Start the main function
if __name__ == "__main__":
   main()
