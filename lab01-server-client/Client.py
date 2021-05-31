from os import system
from socket import *


class Client:

    def __init__(self, server_name, server_port):
        self.create_socket(server_name, server_port)


    def create_socket(self, server_name, server_port):
        self.__client_socket = socket(AF_INET, SOCK_STREAM)
        self.__client_socket.connect((server_name, server_port))

       
    def send_data(self, data):
        self.__client_socket.send(data.encode())


    def receive_data(self):
        return self.__client_socket.recv(1024).decode()


    def close_connection(self):
        self.__client_socket.close()


if __name__ == "__main__":
    serverName = '127.0.0.1'
    serverPort = 12000

    while True:
    
        my_cli = Client(serverName, serverPort)

        
        sentence = input("\n>>> ")

        # el cliente puede enviar:
        #  -LIST lista los ficheros en el directorio donde se ejecuta el server
        #  -GET <FILE> devuelve el archivo FILE en el directorioa del server
        #  -METADATA <FILE> devuelve metadata del FILE en el dir del server
        #  -CLOSE cierra la conexion entre las partes

        my_cli.send_data(sentence)
        response = my_cli.receive_data()
        if response == "CLOSE":
            print(f"From Server: \n Connection finished...")
            input("Press enter to continue...")
            break

        else:
            print(f"From Server: \n{response}")
    
            my_cli.close_connection()
        input("Press enter to continue...")
        system("clear")




