import pika
import time
import json
import threading
import datetime

clients = {}
mensajes = []
def escribirEnLog(texto):
    f = open("log.txt","a")
    f.write(texto)
    f.close()

def on_request(ch, method, properties, body):
    global mensajes
    global clients
    request = json.loads(body)

    message = {}
    if request['option'] == 0:
        if request['username'] not in clients:
            clients[request['username']] = request['queue_name']
            message = json.dumps({
                'option': 0,
                'username': request['username']
            })

        elif request['username'] in clients:
            message = json.dumps({
                'option': 0,
                'username': None
            })

    elif request['option'] == 1:
        message = json.dumps({
            'option': 1,
            'clients': list(clients.keys())
        })

    elif request['option'] == 2:
        try:
            if request['receiver'] in clients:

                mensajes.append(request)
                message = json.dumps({
                    'option': 2,
                    'message': request['message'],
                    'emisor': request['username']
                })
                tiempo =  time.time()
                tiempo = datetime.datetime.fromtimestamp(tiempo).strftime('%d-%m-%Y %H:%M:%S')

                temp = "{}\n{}->{}:{}\n".format(tiempo,request['username'],request['receiver'],request['message'])
                print(temp)
                escribirEnLog(temp)
                channel.basic_publish(
                    exchange='clients',
                    routing_key=clients[request['receiver']],
                    body=message)

                return
            else:
                message = json.dumps({
                'option': 2,
                'message': None
                })
        except:
            message = json.dumps({
                'option': 2,
                'message': None
            })
    elif request['option'] == 3:
        todos = []
        for msn in mensajes:
            if msn['username'] == request['username']:
                todos.append(msn)
        message = json.dumps({
            'option': 3,
            'mensajes': todos
        })
        channel.basic_publish(
                exchange='clients',
                routing_key=clients[request['username']],
                body=message)

    channel.basic_publish(
        exchange='clients',
        routing_key=request['queue_name'],
        body=message)

    ch.basic_ack(delivery_tag=method.delivery_tag)


# canal de intercambio para enviar mensajes a clientes
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='clients', exchange_type='direct')


# Canal que recibe las entradas de los clientes
connectionServer = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channelServer = connectionServer.channel()

channelServer.queue_declare(queue='queueServidor')

channelServer.basic_consume(queue='queueServidor',
                            on_message_callback=on_request)

channelServer.start_consuming()
