import select
import socket
from CommandUtils import CommandUtils as CommandU

server_ip = "localhost"
server_port = 20001
listen = 5
welcome_msg = "Welcome!!!\nType HELP to see the command list."


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, server_port))
server.listen(listen)

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
        if e is server: # Server actions
            connection, direccion = e.accept()
            print("Conexion establecida con el cliente", direccion)
            connection.send(welcome_msg.encode())
            connection.setblocking(0)
            inputs.append(connection)
        else: # Connection socket actions
            commandU = CommandU(e)
            data = e.recv(1024)
            if data:
                message = data.decode()
                connection_port = e.getpeername()
                print("Mensaje recibido:", message, "from", connection_port)
                msg_words = message.split()
                response = commandU.switch(*msg_words)
                e.send(response.encode())



    # Manejo de salidas

    for s in salidas:
        print(s)

    # Manejo de errores

    for e in errores:
        pass