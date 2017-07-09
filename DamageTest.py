# Demo program to show how to Handle damage

from damage import damageAllocation

import tkinter as tk
from samplegame import sampleGame

# PURPOSE:
#  create bare page
# RETURNS: none
def main():
    lists = sampleGame['objects']
    shipList = lists['shipList']
    ship = shipList[0]
    ship['damage'] = 5

    root = tk.Tk()
    root.title("testDamage")
    damageAllocation(root, ship)
    root.mainloop()

# Start the main function
if __name__ == "__main__":
   main()


