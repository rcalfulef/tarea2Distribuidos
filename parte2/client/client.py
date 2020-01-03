import pika
import json
import time
import threading
import uuid 

address = 'localhost'
port = 280414

username = None

def callback(ch, method, properties, body):
    global username
    resp = json.loads(body)

    if resp['option'] == 0:
        if resp['username'] != None:
            username = resp['username']
            print("Bienvenido, {}\n".format(username))
        if resp['username'] == None:
            print("El usuario ya existe")   

    elif resp['option'] == 1:
        print("\nClientes:")
        for i in resp['clients']:
            print(i)
        print('')

    elif resp['option'] == 2:
        if resp['message'] != None:
            print("{}:{}".format(resp['emisor'], resp['message']))

        elif resp['message'] == None:
            print("el usuario no existe, por favor intenta con otro: ")
           
    elif resp['option'] == 3:
        print("mensajes enviador por mi:")
        cont= 1
        for msn in resp['mensajes']:
            print('{}.- para {}: {}'.format(cont,msn['receiver'],msn['message']))
            cont+=1
        print('')

def printOpciones():
    print("Selecciona alguna de las siguientes opciones")
    print("1. ver lista de clientes")
    print("2. enviar un mensaje a cliente")
    print("3. Mostar mis mensajes enviados")
    print("4. Salir")

def __listen__for__messages():
    channel.start_consuming()

# se crea un canal hacia el servidor, se creara el canal hacia el cliente, despues de asignar el nombre del cliente
connectionServer = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channelServer = connectionServer.channel()
channelServer.queue_declare(queue='queueServidor')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='clients', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)

queue_name = result.method.queue
# se enlaza la cola creada al exchange clientes
channel.queue_bind(exchange='clients', queue=queue_name)

channel.basic_consume(
    queue=queue_name,
    auto_ack=True,
    on_message_callback=callback
)
threading.Thread(target=__listen__for__messages, daemon=True).start()

while username == None:
    temp = input("Ingrese nombre de usuario: ")
    x = {
        'option': 0,
        'username': temp,
        'queue_name': queue_name
    }
    message = json.dumps(x)
    channelServer.basic_publish(
        exchange='',
        routing_key='queueServidor',
        body=message)
    time.sleep(0.2)

printOpciones()
opcion = input("")
while(opcion != '4'):
    if opcion == '1':
        message = json.dumps({
        'option': 1,
        'username': username,
        'queue_name': queue_name
    })

        channelServer.basic_publish(
            exchange='',
            routing_key='queueServidor',
            body=message)
    
    elif opcion == '2':
        nombreUsuario = input(
            'ingrese el nombre de usuario al que enviara mensaje: ')
        mensaje = input('mensaje: ')
        message = json.dumps({
            'option': 2,
            'receiver': nombreUsuario,
            'message': mensaje,
            'username': username,
            'queue_name': queue_name,
            'id': uuid.uuid1().int
        })
        channelServer.basic_publish(
            exchange='',
            routing_key='queueServidor',
            body=message)
    elif opcion == "3":
        message = json.dumps({
            'option': 3,
            'username': username,
            'queue_name': queue_name
        })
        
        channelServer.basic_publish(
            exchange='',
            routing_key='queueServidor',
            body=message)
    else:
        print('ingrese una opcion valida')
    time.sleep(0.2)    

    print("\n\nSelecciona alguna de las siguientes opciones")
    print("1. ver lista de clientes")
    print("2. Enviar un mensaje")
    print("3. Mostar mis mensajes enviados")
    print("4. Salir")
    opcion = input("Opcion: ")