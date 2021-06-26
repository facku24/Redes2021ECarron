import select
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 22000))
server.listen(1)

inputs = [server, ]
outputs = []
errors = []

print("socket del servidor:", server.fileno())

while True:
    read_list, write_list, err_list = select.select(inputs, outputs, errors)


    for item in read_list:
        if item is server:
            client, address = item.accept()

            print("Oye, alguien ha establecido una conexión contigo:", client.fileno())
            inputs.append(client)
        else:
            msg = item.recv(1024)
            if msg != b'':
                print(f"Mensaje {item.getsockname()} recibido: {msg.decode()}")

                if item not in outputs:
                    outputs.append(item)
            # else:
            #     print(f"No es bueno, {item.fileno()} se ha ido")
            #     if item in outputs:
            #         outputs.remove(item)
            #     inputs.remove(item)
            #     item.close()

    for item in outputs:
        item.send(f"Hola! {item.fileno()} Hola, he recibido tu mensaje".encode())
        print("¡El mensaje ha sido enviado!")
        outputs.remove(item)

    for item in errors:
        print(f"¡Listo, {item.fileno()} es anormal!")
        inputs.remove(item)
        if item in outputs:
            outputs.remove(item)

