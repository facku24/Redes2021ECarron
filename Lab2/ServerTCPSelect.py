import select
from Server import Server

server_ip = "localhost"
server_port = 20001
listen = 5

server = Server(server_ip, server_port, listen)

# Sockets desde los cuales vamos a leer

inputs = [server]

# Sockets hacia los cuales vamos a escribir

outputs = []

# Sockets de errores

errors = []

# print("Servidor funcionando...")

while inputs:
    entradas, salidas, errores = select.select(inputs, outputs, errors)

    # Manejo de entradas
    for e in entradas:
        if e is server:
            e.accept_connection()
            connection = e.get_connection_socket()
            direction = e.get_client_addr()
            # connection, direction = e.accept_connection()
            print("Conexion establecida con el cliente", direction)
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
        pass

    # Manejo de errores

    for e in errores:
        pass