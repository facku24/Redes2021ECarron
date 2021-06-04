from socket import *
from os import listdir, scandir
from datetime import datetime

class Server:
		
		
	def __init__(self, server_name, server_port):
		self.create_socket(server_name, server_port)
		self.__client_addr = None


	def create_socket(self, server_name, server_port):
		self.__server_socket = socket(AF_INET, SOCK_STREAM)
		self.__server_socket.bind((server_name, server_port))
		self.__server_socket.listen(1)
		print("The server is ready to receive")
		#print(f"The server " + ";".join([k for k,v in globals().items if v is self]) + " is ready to receive")


	def receive_data(self):
		self.__conn_socket, self.__client_addr = self.__server_socket.accept()#tiene que ir aparte?
		return self.__conn_socket.recv(1024).decode()
		
		
	def send_data(self, data):
		self.__conn_socket.send(data.encode())
		


	def close_socket(self):
		self.__conn_socket.close()
#-----------------------------------------------

def list_files():
	response = listdir()
	return '\n'.join(response)

def get_file(file):
	try:
		f = open(f"{file}")
		lines = f.readlines()
		response = "".join(lines)
	except IOError as e:
		response = "El archivo no existe"
	finally:
		f.close()
		return response

def get_file_metadata(file):
	filesDir = list(scandir())

	fileObj = None
	for i in filesDir:
		if i.name == file:
			fileObj = i
			break

	metadataValues = tuple(fileObj.stat())

	return f"""
	{fileObj.name} metadata info:

	Mode: {metadataValues[0]},
	Inode Number: {metadataValues[1]},
	Device Id: {metadataValues[2]},
	Hard Links: {metadataValues[3]},
	User Id: {metadataValues[4]},
	Group Id: {metadataValues[5]},
	Size: {metadataValues[6]} bytes,
	Access Time: {datetime.fromtimestamp(metadataValues[7]).strftime("%A, %B %d, %Y %I:%M:%S")},
	Modification Time: {datetime.fromtimestamp(metadataValues[8]).strftime("%A, %B %d, %Y %I:%M:%S")},
	Last Metadata Change: {datetime.fromtimestamp(metadataValues[9]).strftime("%A, %B %d, %Y %I:%M:%S")}"""


def close_socket():
	return "CLOSE"

if __name__ == "__main__":
	server_ip = '127.0.0.1'
	server_port = 12000

	query_dict = {
		'LIST': list_files,
		'GET': get_file,
		'METADATA': get_file_metadata,
		'CLOSE': close_socket
	}

	my_server = Server(server_ip, server_port)

	
	
	while True:
		sentence = my_server.receive_data().split(' ')
		
	# el servidor debe enviar:
    #  -LIST lista los ficheros en el directorio donde se ejecuta el server
	#		encabezado = resultado de la operacion, tantas lineas como archivos en el dir
    #  -GET <FILE> devuelve el archivo FILE en el directorioa del server
	#		encabezado = resultado de la operacion, el archivo mismo
    #  -METADATA <FILE> devuelve metadata del FILE en el dir del server
	#		encabezado = resultado de la operacion, el archivo mismo
    #  -CLOSE cierra la conexion entre las partes
	#		encabezado = resultado de la operacion, terminar la conexion
	#print([i[0] for i in locals().items() if self is i[1]])
	

		if len(sentence) == 1 and sentence[0] in query_dict:
			response = query_dict[sentence[0]]()
		elif len(sentence) == 2 and sentence[0] in query_dict:
			try:
				response = query_dict[sentence[0]](sentence[1])
			except:
				response = "Error, ilegal arguments"
			
		else:
			response = ' '.join(sentence).upper()

		if response == "CLOSE":
			my_server.send_data(response)
			my_server.close_socket()
			break
		else:
			my_server.send_data(response)
			my_server.close_socket()