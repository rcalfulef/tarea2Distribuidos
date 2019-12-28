import pika
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello',durable=True)

def callback(ch,method,properties,body):
    print("se recibio, %r" % body)
    time.sleep(body.count(b'.'))
    print('hecho')
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='hello', on_message_callback = callback)

print('esperando por mensajes. presiona ctrl+c para salir')

channel.start_consuming()

