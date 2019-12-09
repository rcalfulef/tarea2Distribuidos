import grpc
from concurrent import futures
import time


import chat_pb2
import chat_pb2_grpc

class ChatServicer(chat_pb2_grpc.ChatServicer):
    def EnviarMensaje(self, request, context):
         response = chat_pb2.Mensaje()
         return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

chat_pb2_grpc.add_ChatServicer_to_server(
    ChatServicer(),server)

print("Iniciando servidor. Escuchando en el puerrto 50052")
server.add_insecure_port('[::]:50052')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
