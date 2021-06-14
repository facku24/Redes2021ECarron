from socket import *
from CommandUtils import CommandUtils as CU

class Server:

    def __init__(self, ip_addr, port, listen=1):
        self.__server_socket = socket(AF_INET, SOCK_STREAM)
        self.__server_socket.bind((ip_addr, port))
        self.__server_socket.listen(listen)
        self.__connection_socket = None
        self.__client_addr = None
        print("The server is ready to receive")

    def get_client_addr(self):
        return self.__client_addr

    def get_connection_socket(self):
        return self.__connection_socket

    def accept_connection(self):
        self.__connection_socket, self.__client_addr = self.__server_socket.accept()

    def receive_data(self):
        return self.__connection_socket.recv(1024)

    def receive_decoded_data(self):
        return self.__connection_socket.recv(1024).decode()

    def send_data(self, data):
        self.__connection_socket.send(data)

    def send_encoded_data(self, data):
        self.__connection_socket.send(data.encode())

    def close_connection_socket(self):
        self.__connection_socket.close()


# el servidor debe enviar:
#  -LIST lista los ficheros en el directorio donde se ejecuta el server
#		encabezado = resultado de la operacion, tantas lineas como archivos en el dir
#  -GET <FILE> devuelve el archivo FILE en el directorioa del server
#		encabezado = resultado de la operacion, el archivo mismo
#  -METADATA <FILE> devuelve metadata del FILE en el dir del server
#		encabezado = resultado de la operacion, el archivo mismo
#  -CLOSE cierra la conexion entre las partes
#		encabezado = resultado de la operacion, terminar la conexion


if __name__ == "__main__":
    server_ip = '127.0.0.1'
    server_port = 12005

    my_server = Server(server_ip, server_port)
    while True:
        my_server.accept_connection()
        my_server.send_encoded_data("Welcome!!!\n"
                                    "Type HELP to see the command list.")
        while True:
            server_command = CU(my_server.get_connection_socket())
            sentence = my_server.receive_decoded_data().split(' ')
            response = server_command.switch(*sentence)
            my_server.send_encoded_data(response)
            if response == 'Good bye...':
                my_server.close_connection_socket()
                break
