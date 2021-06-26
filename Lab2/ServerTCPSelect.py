import select
import socket
from CommandUtils import CommandUtils as CommandU

server_ip = "localhost"
server_port = 20000
listen = 5
messages = {}  # OJO. Ver creciimento de este objeto.
welcome_msg = "Welcome!!!\nType HELP to see the command list."
closing_msg = "Good bye..."


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

    # Input handling

    for input_socket in entradas:
        if input_socket is server: # Server actions
            connection, direction = input_socket.accept()

            print("Conexion establecida con el cliente", direction)

            # connection.setblocking(0) purpose of this line?

            inputs.append(connection)
        else:
            msg = input_socket.recv(1024)
            connection_port = input_socket.getpeername()[1]

            if msg:  # != b'': manejar msj vacio desde el server????
                message = msg.decode()
                print("Mensaje recibido:", message, "from", connection_port)
                messages[connection_port] = msg.decode()

                if input_socket not in outputs:
                    outputs.append(input_socket)

            # cierra el socket si el msj esta vacio.
            # else:
            #     print(f"No es bueno, {item.fileno()} se ha ido")
            #     if item in outputs:
            #         outputs.remove(item)
            #     inputs.remove(item)
            #     item.close()

    # Output Handling

    for output_socket in salidas:
        socket_no = output_socket.getpeername()[1]

        if messages[socket_no] == "Yippee-Ki-Yay":
            messages[socket_no] = ''
            output_socket.send(welcome_msg.encode())
            print("¡El mensaje de bienvenida ha sido enviado!")

        else:
            command_handler = CommandU(output_socket)
            request_words = messages[socket_no].split(' ')
            response = command_handler.switch(*request_words)

            if response == 'Good bye...':
                output_socket.send(closing_msg.encode())
                print("¡El mensaje de despedida ha sido enviado!")

                if output_socket in inputs:
                    inputs.remove(output_socket)
                output_socket.close()
                del messages[socket_no]  # keeps the message dictionary clean

            else:
                output_socket.send(response.encode())
                print("¡El mensaje ha sido enviado!")

        outputs.remove(output_socket)

    # Error handling

    for error_socket in errores:
        pass