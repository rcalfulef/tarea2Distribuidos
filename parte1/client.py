import threading
from tkinter import *
from tkinter import simpledialog

import grpc

import chat_pb2 as chat
import chat_pb2_grpc as rpc

import time
from datetime import datetime

address = 'localhost'
port = 280414

class Client:
    def __init__(self):
        self.username = None
        # se crea el canar grpc
        channel = grpc.insecure_channel(address + ':' + str(port))
        self.conn = rpc.ChatStub(channel)
        self.agregarCliente()
        print("\nBienvenido {}!".format (self.username))
        print("Selecciona alguna de las siguientes opciones")
        print("1. ver lista de clientes")
        print("2. enviar un mensaje a cliente")
        print("3. Mostar mis mensajes enviados")
        print("4. Salir")

        threading.Thread(target=self.__listen__for__messages, daemon=True).start()
        
        opcion = input("Opcion: ")
        while(opcion != '4'):
            if opcion == '1':
                print('\n\nclientes conectados:')
                self.listaClientes()
            elif opcion == '2':
                print('Seleccione alguno de los siguientes clientes')
                self.listaClientes()
                clientSelect = input("Nombre del cliente receptor: ")
                message = input("Mensaje: ")
                m = chat.Mensaje()
                m.id = "1"
                m.mensaje = message
                m.timestamp = time.time()
                m.usernameEmisor = self.username
                m.usernameReceptor = clientSelect
                code = self.conn.EnviarMensaje(m)
                if code.value == 2:
                    print("el usuario no existe ")
                elif code.value ==3:
                    print("un error a ocurrido intentelo nuevamente")

            elif opcion == "3":
                self.mensajesEnviados()

            else:
                print('ingrese una opcion valida')

            print("\n\nSelecciona alguna de las siguientes opciones")
            print("1. ver lista de clientes")
            print("2. Enviar un mensaje")
            print("3. Mostar mis mensajes enviados")
            print("4. Salir")
            opcion = input("Opcion: ")


    def __listen__for__messages(self):
        """funcion que se encarga de mostrar los mensajes solo si el destinatario es el usuario actual"""
        for note in self.conn.ChatStream(chat.Vacio()):
            if note.usernameReceptor == self.username:
                print("\nMensaje recibido de {}: {}\n".format(note.usernameEmisor, note.mensaje))
                print("opcion:")
            
    def agregarCliente(self):
        while self.username == None:
            temp = input("Ingrese nombre de usuario: ")
            c = chat.Cliente()
            c.username = temp
            code = self.conn.AgregarCliente(c).value
            if code == 1:
                self.username = temp
                return temp
            elif code == 2:
                print("un error a ocurrido intentalo nuevamente")
            elif code == 3:
                print('Este usuario ya existe, prueba con otro nombre')
            

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

    def listaClientes(self):
        cont = 1
        
        for cliente in self.conn.ListadoClientes(chat.Vacio()):
            print("{}. {}".format(cont,cliente.username))
            cont+=1

    def mensajesEnviados(self):

        c = chat.Cliente()
        c.username = self.username
        for mensaje in self.conn.MensajesEnviadosPor(c):
            print("{}: {}".format(mensaje.usernameReceptor,mensaje.mensaje))

    


        
if __name__  == '__main__':
    c = Client() 