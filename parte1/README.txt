INSTALACION

Para ejecutar el programa, debe instalarse pipenv con el comando "sudo pip install pipenv", luego activamos el entorno con "pipenv shell" en la misma carpeta donde se encuentra el archivo Pipfile

Para instalar las dependencias ejecutar "pipenv install", 
con esto se instalaran todas las librearias necesarias para el funcionamiento de la app

EJECUTAR

Para ejecutar el programa realizaremos lo siguiente:

SERVIDOR
se debe comenzar por el servidor, luego de crear y activar el entorno. ejecutaremos "py server.py", con esto el servidor estara a la espera

CLIENTES
Luego de que el servidor este funcionando, podemos ejecutar los clientes, para esto ejecutaremos el comando "py client.py"

se desplegara el menu para poder realizar las diferentes acciones, tener en consideracion que para enviar un mensaje a otro cliente se debe ingresar su nombre, por ejemplo:

Seleccione alguno de los siguientes clientes
1. juan
2. pepe
Nombre del cliente receptor: --> juan <------------