import pika
import json
import time

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

class Client:
    def __init__(self):
        self.username = None

        connectionServer = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channelServer = connectionServer.channel()
        # se crea un canal hacia el servidor, se creara el canal hacia el cliente, despues de asignar el nombre del cliente
        channelServer.queue_declare(queue='queueServidor', durable=True)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        
        nombreCola = result.method.queue
        self.agregarCliente(channelServer,channel,nombreCola)




        print("\nBienvenido {}!".format(self.username))
        print("Selecciona alguna de las siguientes opciones")
        print("1. ver lista de clientes")
        print("2. enviar un mensaje a cliente")
        print("3. Mostar mis mensajes enviados")
        print("4. Salir")

    #     threading.Thread(target=self.__listen__for__messages,
    #                      daemon=True).start()

        

    # def __listen__for__messages(self):
    #     """funcion que se encarga de mostrar los mensajes solo si el destinatario es el usuario actual"""
    #     for note in self.conn.ChatStream(chat.Vacio()):
    #         if note.usernameReceptor == self.username:
    #             print("Mensaje recibido de {}: {}".format(
    #                 note.usernameEmisor, note.mensaje))

    def agregarCliente(self,channelServer,channel,nombreCola):
        while self.username == None:
            temp = input("Ingrese nombre de usuario: ")
            x = {
                'option': 1,
                'username': temp,
                'nombreCola': nombreCola
            }
            message = json.dumps(x)

            channelServer.basic_publish(
                exchange='',
                routing_key='queueServidor',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ))
            
            
            channel.basic_consume(
                queue = nombreCola,
                on_message_callback=callback
            )

            print(" [x] Sent %r" % message)
            


if __name__ == '__main__':
    c = Client()


connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))

channel = connection.channel()
