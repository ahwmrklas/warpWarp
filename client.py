#
# Demo program to show how to connect to WarpWar server
#
import socket         # Import socket module
import tkinter as tk
import threading
import queue as Q


# Socket thread
class comThrd(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self, hGui):
        self.Q = Q.Queue()
        self.hGUI = hGui
        threading.Thread.__init__(self)
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
        print("client ", ip, port, msg, "\n")
        s = socket.socket()
        s.connect((ip, port))
        s.send(msg.encode())
        cmd = s.recv(1024)
        print("client " + cmd.decode())
        s.close()
        self.hGUI.displayCmd(cmd)

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

# GUI thread
class myWindow(threading.Thread):

    # PURPOSE: Called for class construction
    # RETURNS: none
    def __init__(self):
        self.Q = Q.Queue()        
        self.hCOM = comThrd(self)
        threading.Thread.__init__(self)
        self.start()

    # PURPOSE: Called back for quit. Clean up socket and self
    # RETURNS: none
    def quitCB(self):
        self.hCOM.quitCmd()
        self.root.quit()
        print("Client Gui exit")

    # PURPOSE: Send data via the client socket thread
    # RETURNS: none
    def sendMsg(self):
        # print(self.ip, self.port, self.msg)
        self.hCOM.sendCmd(self.ip.get(), int(self.port.get()), self.msg.get())
       
    # PURPOSE: Construct all the GUI junk
    # RETURNS: nothing
    def initGui(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.protocol("WM_DELETE_WINDOW", self.quitCB)

        tmp = tk.Label(self.root, text="Client: ")
        tmp.grid(row=1, column=0)

        host = socket.gethostname()
        tmp = tk.Label(self.root, text=host)
        tmp.grid(row=1, column=1)

        tmp = tk.Label(self.root, text="Send IP: ")
        tmp.grid(row=2, column=0)
        
        self.ip = tk.StringVar()
        self.ip.set(host)
        self.ipEntry = tk.Entry(self.root, textvariable=self.ip)
        self.ipEntry.grid(row=2, column=1)

        tmp = tk.Label(self.root, text="Send Port: ")
        tmp.grid(row=3, column=0)

        self.port = tk.StringVar()
        self.port.set('12345')
        self.portEntry = tk.Entry(self.root, textvariable=self.port)
        self.portEntry.grid(row=3, column=1)

        tmp = tk.Label(self.root, text="Send Msg: ")
        tmp.grid(row=4, column=0)

        self.msg = tk.StringVar()
        self.msg.set("hi")
        self.msgEntry = tk.Entry(self.root, textvariable=self.msg)
        self.msgEntry.grid(row=4, column=1)

        tmp = tk.Button(self.root, text="Send", command=self.sendMsg)
        tmp.grid(row=5, column=1)

        tmp = tk.Label(self.root, text="Resp Msg: ")
        tmp.grid(row=7, column=0)

        self.resp = tk.StringVar()
        self.resp.set("")
        self.respEntry = tk.Entry(self.root, textvariable=self.resp)
        self.respEntry.grid(row=7, column=1)    

    # PURPOSE: for external parties to send a message to the GUI thread
    #          The socket client uses this
    # RETURNS: none
    def displayCmd(self, msg):
        self.Q.put(msg)

    # PURPOSE: drain the Q
    #    While this returns. It also starts a timer
    #    that will call this function again
    # RETURNS: none
    def poll(self):
        while not self.Q.empty():
            self.resp.set(self.Q.get())
        self.root.after(2000, self.poll)

    # PURPOSE: automatically called by base thread class, right?
    #     create the GUI, wait for msgs on a timer, run the tkinter
    #     thing so the GUI responds to the user
    # RETURNS: none
    def run(self):
        self.initGui()
        self.poll()
        self.root.mainloop()

# PURPOSE: start up stuff...
# RETURNS: none?
def main():
    lDLG = myWindow()
    print("two threads created main program exit")


# Start the main function
if __name__ == "__main__":
   main()
