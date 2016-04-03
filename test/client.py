import socket         # Import socket module
import tkinter as tk
import threading
import queue as Q


class comThrd(threading.Thread):

    def __init__(self):
        self.Q = Q.Queue()
        threading.Thread.__init__(self)
        self.start()

    def sendCmd(self, ip, port, msg):
        self.Q.put("send")
        self.Q.put(ip)
        self.Q.put(port)
        self.Q.put(msg)

    def quitCmd(self):
        self.Q.put("quit")
        
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
        gDLG.displayCmd(cmd)

    def handleQuit(self):
        print("comThrd-quit command")

    def run(self):
        while True:
            cmd = self.Q.get()
            if cmd == "send":
                self.handleSend()
            elif cmd == "quit":
                self.handleQuit()
                break

        print("client comThrd exiting")

class myWindow(threading.Thread):

    def __init__(self):
        self.Q = Q.Queue()        
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        gCOM.quitCmd()
        self.root.quit()
        print("Client Gui exit")

    def connect(self):
        # print(self.ip, self.port, self.msg)
        gCOM.sendCmd(self.ip.get(), int(self.port.get()), self.msg.get())
       
    def initGui(self):
        self.root = tk.Tk()
        self.root.title("Client")
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

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

        tmp = tk.Button(self.root, text="Send", command=self.connect)
        tmp.grid(row=5, column=1)

        tmp = tk.Label(self.root, text="Resp Msg: ")
        tmp.grid(row=7, column=0)

        self.resp = tk.StringVar()
        self.resp.set("")
        self.respEntry = tk.Entry(self.root, textvariable=self.resp)
        self.respEntry.grid(row=7, column=1)    

    def displayCmd(self, msg):
        self.Q.put(msg)

    def poll(self):
        while not self.Q.empty():
            self.resp.set(self.Q.get())
        self.root.after(2000, self.poll)

    def run(self):
        self.initGui()
        self.poll()
        self.root.mainloop()


gCOM = comThrd()
gDLG = myWindow()
print("two threads created main program exit")

