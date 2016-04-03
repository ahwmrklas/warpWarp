import socket               # Import socket module
import tkinter as tk
import threading
import queue as Q

class srvrThrd(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def setSendMsgCmd(self, msg):
        # this is not thread safe. Need to put in Q
        self.sendMsg = msg.encode()
        #print (self.sendMsg.encode())
        
    def run(self):
        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        s.bind((host, port))

        s.listen(5)
        while True:
           c, addr = s.accept()

           c.send(self.sendMsg)
           cmd = c.recv(1024)
           print("server " + cmd.decode())
           c.close()
           gGUI.displayAddr(addr)
           gGUI.displayMsg(cmd.decode())
           if cmd == b'quit':
               break
        print("socket listen exiting")

class MyTkApp(threading.Thread):
    
    def __init__(self):
        self.Q = Q.Queue()
        threading.Thread.__init__(self)
        self.start()
        
    def callback(self):
        self.root.quit()
        print("Server Gui exit")

    def initGui(self):
        self.root = tk.Tk()
        self.root.title("Server IP:port")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        tmp = tk.Label(self.root, text="Server: ")
        tmp.grid(row=1, column=0)

        host = socket.gethostname()
        port = '12345'
        tmp = tk.Label(self.root, text=host+":"+port)
        tmp.grid(row=1, column=1)
        
        tmp = tk.Label(self.root, text="Send Msg: ")
        tmp.grid(row=3, column=0)
        
        self.sendMsg = tk.StringVar()
        self.sendMsg.set("")
        self.sendMsgEntry = tk.Entry(self.root, textvariable=self.sendMsg)
        self.sendMsgEntry.grid(row=3, column=1)
        
        tmp = tk.Label(self.root, text="Received From: ")
        tmp.grid(row=5, column=0)
        
        self.recvFrom = tk.StringVar()
        self.recvFrom.set("")
        self.recvFromEntry = tk.Entry(self.root, textvariable=self.recvFrom)
        self.recvFromEntry.grid(row=5, column=1)

        tmp = tk.Label(self.root, text="Received Msg: ")
        tmp.grid(row=6, column=0)
        
        self.recvMsg = tk.StringVar()
        self.recvMsg.set("")
        self.recvMsgEntry = tk.Entry(self.root, textvariable=self.recvMsg)
        self.recvMsgEntry.grid(row=6, column=1)

    def displayAddr(self, msg):
        self.Q.put("addr")
        self.Q.put(msg)
        
    def displayMsg(self, msg):
        self.Q.put("msg")
        self.Q.put(msg)        

    def handleDisplayAddr(self):
        addr = self.Q.get()
        self.recvFrom.set(addr)
        
    def handleDisplayMsg(self):
        msg = self.Q.get()
        self.recvMsg.set(msg)
        
    def poll(self):
        gNET.setSendMsgCmd(self.sendMsg.get())
        while not self.Q.empty():
            cmd = self.Q.get()
            if (cmd == "addr"):
                self.handleDisplayAddr()
            elif (cmd == "msg"):
                  self.handleDisplayMsg()
        self.root.after(2000, self.poll)
    
    def run(self):
        self.initGui()
        self.poll()
        self.root.mainloop()


gGUI = MyTkApp()
gNET = srvrThrd()
print("two threads created. Main program exiting")
