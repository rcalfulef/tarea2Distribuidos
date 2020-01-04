from concurrent import futures

import grpc
import time

import chat_pb2 as chat
import chat_pb2_grpc as rpc
import datetime

def escribirEnLog(texto):
    f = open("log.txt","a")
    f.write(texto)
    f.close()

class ChatServer(rpc.ChatServicer):

    def __init__(self):
        self.chats = []     # lista de mensajes
        self.clients = []   # lista de clientes
    

    def ChatStream(self, request_iterator, context): # funcion encargada de entregar los mensajes a los clientes  
        ultimoIndice = 0
        while(True):
            while (len(self.chats)) > ultimoIndice: # se verifica si hay nuevos mensajes
                mensaje = self.chats[ultimoIndice]
                ultimoIndice += 1
                yield mensaje

    def AgregarCliente(self, request:chat.Cliente, context):
        try:
            if request not in self.clients:
                self.clients.append(request)
                return chat.MensajeReply(value = 1) # se retorna 1 si el cliente se agrego con exito
            else: 
                return chat.MensajeReply(value = 3) # si el cliente ya existe
        except:
            return chat.MensajeReply(value = 2) # otro error

    def EnviarMensaje(self, request: chat.Mensaje, context):
        """recibe un mensaje desde algun cliente y lo guarda en la lista de mensajes"""
        try:
            for client in self.clients:
                if request.usernameReceptor == client.username:
                    tiempo = datetime.datetime.fromtimestamp(request.timestamp).strftime('%d-%m-%Y %H:%M:%S')
                    temp = "{}\n{}->{}: {}\n\n".format(tiempo,request.usernameEmisor,request.usernameReceptor, request.mensaje) 
                    print(temp)
                    escribirEnLog(temp)            
                    self.chats.append(request)
                    return chat.MensajeReply(value = 1)
            
            return chat.MensajeReply(value = 2)
        except:
            return chat.MensajeReply(value = 3)

    def ListadoClientes(self, request: chat.Vacio, context):
        for cliente in self.clients:
            yield cliente
    
    def MensajesEnviadosPor(self, request: chat.Cliente,context):
        for mensaje in self.chats:
            if mensaje.usernameEmisor == request.username:
                yield mensaje


if __name__ == '__main__':
    port = 280414  # puerto del servidor
    server = grpc.server(futures.ThreadPoolExecutor(
        max_workers=10))  # servidor grpc que soporta 10 clientes
    rpc.add_ChatServicer_to_server(ChatServer(), server)
    print("Iniciando servidor. Escuchando en el puerto {}".format(port))
    server.add_insecure_port('[::]:' + str(port))
    server.start()
    while True: # las hebras que esperan mensajes estaran activas, se utiliza este while para que no se cierre el hilo padre
        time.sleep(64 * 64 * 100)