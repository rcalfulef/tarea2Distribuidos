import grpc

import chat_pb2
import chat_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')

stub = chat_pb2_grpc.ChatStub(channel)

mensaje = chat_pb2.Mensaje(value= "buenaa")

response = stub.EnviarMensaje(mensaje)

print(response)