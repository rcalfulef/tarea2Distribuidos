from concurrent import futures

import grpc
import time

import chat_pb2 as chat
import chat_pb2_grpc as rpc


class ChatServer(rpc.ChatServicer):

    def __init__(self):
        # lista de mensajes
        self.chats = []

    def ChatStream(self, request_iterator, context):
        """
        This is a response-stream type call. This means the server can keep sending messages
        Every client opens this connection and waits for server to send new messages

        :param request_iterator:
        :param context:
        :return:
        """
        ultimoIndice = 0
        # For every client a infinite loop starts (in gRPC's own managed thread)
        while(True):
            # Check if there are any new messages
            while (len(self.chats)) > ultimoIndice:
                mensaje = self.chats[ultimoIndice]
                ultimoIndice += 1
                yield mensaje

    def EnviarMensaje(self, request: chat.Mensaje, context):
        """
        This method is called when a clients sends a Note to the server.

        :param request:
        :param context:
        :return:
            
        """
        print("[{}]{}".format(request.name,request.mensaje))
        self.chats.append(request)
        return chat.MensajeReply(1)
        # response = chat_pb2.Mensaje()
        # return response


if __name__ == '__main__':
    port = 280414 # a random port for the server to run on
    # the workers is like the amount of threads that can be opened at the same time, when there are 10 clients connected
    # then no more clients able to connect to the server.
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10)) # create a gRPC server
    rpc.add_ChatServicer_to_server(ChatServer(),server) # register the server to gRPC
    print("Iniciando servidor. Escuchando en el puerrto 280414")
    server.add_insecure_port('[::]:'+ str(port))
    server.start()
    # Server starts in background (in another thread) so keep waiting
    # if we don't wait here the main thread will end, which will end all the child threads, and thus the threads
    # from the server won't continue to work and stop the server
    while True:
        time.sleep(64 * 64 * 100)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

chat_pb2_grpc.add_ChatServicer_to_server(
    ChatServicer(),server)

server.add_insecure_port('[::]:50052')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
