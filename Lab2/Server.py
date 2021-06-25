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

    def fileno(self):
        return self.__server_socket.fileno()

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
