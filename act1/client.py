import grpc

import chat_pb2
import chat_pb2_grpc
import time

def enviarMensaje(stub):
    texto = input("Ingrese un mensaje")
    seconds = time.time()
    stub.EnviarMensaje(chat_pb2.Mensaje(1,texto,seconds,1,2))


def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = chat_pb2_grpc.ChatStub(channel)
        print("-------------- Enviar mensaje --------------")
        enviarMensaje(stub)

        
if __name__  == '__main__':
    run()