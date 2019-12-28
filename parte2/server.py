import pika
import time
import json
import threading

clients = {}

def on_request(ch, method, properties, body):
    x = json.loads(body)
    print(x)
    if x['option'] == 1 and x['username'] not in clients :
        clients[x['username']] = x['nombreCola']
        y = {
                'option': 1,
                'username': x['username']
            }
        message = json.dumps(y)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel= connection.channel()
        channel.queue_declare(queue=x['nombreCola'])
        channel.basic_publish(
            exchange='', 
            routing_key=x['nombreCola'], 
            body=message)
            
        connection.close()

    
    print(clients)
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')



connectionServer = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channelServer = connectionServer.channel()

channelServer.queue_declare(queue='queueServidor', durable=True)

channelServer.basic_consume(queue='queueServidor', on_message_callback=on_request)





channelServer.start_consuming()