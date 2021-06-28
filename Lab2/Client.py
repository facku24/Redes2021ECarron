import argparse
from os import system
from socket import *


class Client:

    def __init__(self, server_name, server_port):
        self.create_socket(server_name, server_port)

    def create_socket(self, server_name, server_port):
        self.__client_socket = socket(AF_INET, SOCK_STREAM)
        self.__client_socket.connect((server_name, server_port))

    def send_data(self, data):
        return self.__client_socket.send(data)

    def send_encoded_data(self, data):
        return self.__client_socket.send(data.encode())

    def receive_data(self):
        return self.__client_socket.recv(1024)

    def receive_decoded_data(self):
        return self.__client_socket.recv(1024).decode()

    def close_connection(self):
        self.__client_socket.close()

    def receive_file(self, file_name):
        lecture = my_cli.receive_data()
        with open(file_name, 'wb') as file:
            while lecture:
                print('Receiving...')
                file.write(lecture)
                if len(lecture) < 1024:
                    break
                lecture = my_cli.receive_data()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process cli args")
    parser.add_argument('--saddr', default="127.0.0.1", type=str, help="Set the server's ip address. Default 127.0.0.1")
    parser.add_argument('--port', default=20000, type=int, help="Set the server's port.\
                        Default port 20000.")

    args = parser.parse_args()

    serverName = args.saddr
    serverPort = args.port

    my_cli = Client(serverName, serverPort)
    system('clear')
    my_cli.send_encoded_data("Yippee-Ki-Yay")

    while True:
        response = my_cli.receive_decoded_data()
        if response == 'Good bye...':
            print(f"From Server: Connection finished...\n{response}\n")
            my_cli.close_connection()
            input("Press <Enter> to exit")
            break
        elif response.split(' ')[0] == 'sending':
            my_cli.receive_file(response.split(' ')[1])
            print('File received...')
        else:
            print(f"From Server:\n\n{response}")

        # Client sending message
        sentence = ''
        while sentence == '':
            sentence = input("\n>>> ")

        if sentence == 'clear()':
            system('clear')

        # el cliente puede enviar:
        #  -LIST lista los ficheros en el directorio donde se ejecuta el server
        #  -GET <FILE> devuelve el archivo FILE en el directorioa del server
        #  -METADATA <FILE> devuelve metadata del FILE en el dir del server
        #  -CLOSE cierra la conexion entre las partes

        my_cli.send_encoded_data(sentence)
