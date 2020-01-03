import pika
import time
import json
import threading

clients = {}
mensajes = []


def on_request(ch, method, properties, body):
    global mensajes
    global clients
    request = json.loads(body)
    print(request)
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

            mensajes.append(request)
            message = json.dumps({
                'option': 2,
                'message': request['message'],
                'emisor': request['username']
            })
            print(message)
            print(clients[request['receiver']])

            channel.basic_publish(
                exchange='clients',
                routing_key=clients[request['receiver']],
                body=message)

            return
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

    print(clients)
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
