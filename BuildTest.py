# Demo program to show how to Handle building

from build import build

import tkinter as tk
from samplegame import sampleGame

# PURPOSE:
#  create bare page
# RETURNS: none
def main():
    lists = sampleGame['objects']
    baseList = lists['starBaseList']
    base = baseList[0]

    root = tk.Tk()
    root.title("testBuild")
    build(root, base)
    root.mainloop()

# Start the main function
if __name__ == "__main__":
   main()

