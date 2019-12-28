import pika


def callback(ch, method, properties, body):
    print("se recibio, %r" % body)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()
channel.queue_declare(queue='task_queue')

channel.basic_consume(queue='task_queue',
                      auto_ack=True,
                      on_message_callback=callback)

print('esperando por mensajes. presiona ctrl+c para salir')

channel.start_consuming()
