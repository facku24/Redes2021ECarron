import select
import socket
import sys
from Lab2.CommandUtils import CommandUtils as CU

param_list = sys.argv

param_dict = {}

for i in range(1, len(param_list) - 1, 2):
    param_dict[param_list[i]] = param_list[i+1]



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 20001))
server.listen(5)

# Sockets desde los cuales vamos a leer

inputs = [server]

# Sockets hacia los cuales vamos a escribir

outputs = []

# Sockets de errores

errors = []

print("Servidor funcionando...")

while inputs:
    entradas, salidas, errores = select.select(inputs, outputs, errors)

    # Manejo de entradas
    for e in entradas:
        if e is server:
            connection, direccion = e.accept()
            print("Conexion establecida con el cliente", direccion)
            connection.setblocking(0)
            inputs.append(connection)
        else:
            data = e.recv(1024)
            if data:
                mensaje = data.decode()
                print("Mensaje recibido:", mensaje)
                e.send(mensaje.upper().encode())


    # Manejo de salidas

    for s in salidas:
        print(s)

    # Manejo de errores

    for e in errores:
        pass