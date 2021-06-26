import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 22000)

print(f"Tengo que establecer una conexión con {server_address}")

client.connect(server_address)

while client:  # True:

    msg = input('>>>')
    client.send(msg.encode())

    data = client.recv(1024)
    print(f"Recibí un mensaje del servidor: {data.decode()}")

    print()  # "Se acabó, quiero cerrarme ~~")
    # client.close()

