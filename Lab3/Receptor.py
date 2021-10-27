from socket import socket
from constantes import *
from paquete import *

destiny = (EMISOR_IP, EMISOR_PORT)

receiver_socket = socket(AF_INET, SOCK_DGRAM)
receiver_socket.bind((RECEPTOR_IP, RECEPTOR_PORT))
print("The server is ready to receive")

while 1:
   incomming_message, network = receiver_socket.recvfrom(LONGITUD_UDP)
   # clienteAddres = (dir_ip, dir_puerto)
   sender, package = loads(incomming_message)
   incomming_data = package.datos #ver como almacenar los datos
   print(package.checksum)
   data = package.datos.upper() if calculo_checksum(package) == 0 else ""
   expected_sec = (package.secuencia + 1) % 2 if calculo_checksum(package) == 0 else package.secuencia
   confirmation_package = Paquete(RECEPTOR_PORT, EMISOR_PORT, data, expected_sec)
   message = dumps((destiny, confirmation_package))
   receiver_socket.sendto(message, (NETWORK_IP, NETWORK_PORT))