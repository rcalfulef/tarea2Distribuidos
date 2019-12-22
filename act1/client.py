import threading
from tkinter import *
from tkinter import simpledialog

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

import time

address = 'localhost'
port = 280414

class Client:
    def __init__(self,u: str,window):
        self.id = id # definimos el id del cliente
        # the frame to put ui components on
        self.window = window
        self.username = u
        # create a gRPC channel + stub
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatStub(channel)
        # create new listening thread for when new message streams come in
        threading.Thread(target=self.__listen__for__messages, daemon=True).start()
        self.__setup_ui()
        self.window.mainloop()

    def __listen__for__messages(self):
        """
        This method will be ran in a separate thread as the main/ui thread, because the for-in call is blocking
        when waiting for new messages
        """
        for note in self.conn.ChatStream(chat.Vacio()):
            print("R[{}] {}".format(note.name, note.message))
            self.chat_list.insert(END,"[{}] {}\n".format(note.idEmisor, note.mensaje))

    

    def enviarMensaje(self,event):
        """
        This method is called when user enters something into the textbox
        """
        mensaje  = self.entry_message.get()

        if mensaje is not '':
            n = chat.Mensaje()
            n.idEmisor = self.username
            n.mensaje = mensaje
            print("S[{}] {}".format(n.idEmisor,n.mensaje))
            self.conn.EnviarMensaje(n)
        # texto = input("Ingrese un mensaje")
        # seconds = time.time()
        # stub.EnviarMensaje(chat_pb2.Mensaje(1,texto,seconds,1,2))

    def __setup_ui(self):
        self.chat_list = Text()
        self.chat_list.pack(side=TOP)
        self.lbl_username = Label(self.window, text=self.username)
        self.lbl_username.pack(side=LEFT)
        self.entry_message = Entry(self.window, bd=5)
        self.entry_message.bind('<Return>', self.enviarMensaje)
        self.entry_message.focus()
        self.entry_message.pack(side=BOTTOM)


        
if __name__  == '__main__':
    root = Tk() # I just used a very simple Tk window for the chat UI, this can be replaced by anything
    frame = Frame(root, width = 300, height = 300)
    frame.pack()
    root.withdraw()
    username = None
    while username == None:
        # retrieve a username so we can distinguish all the different clients
        username = simpledialog.askstring("Username", "What's your username?", parent=root)
    root.deiconify()  # don't remember why this was needed anymore...
    c = Client(username,frame) # this starts a client and thus a thread which keeps connection to server open