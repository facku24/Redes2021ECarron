from time import sleep
from socket import *
from constantes import *
from paquete import Paquete

receiver = (RECEPTOR_IP, RECEPTOR_PORT)

emisor = socket(AF_INET, SOCK_DGRAM)
emisor.bind((EMISOR_IP, EMISOR_PORT))

data = input('Input lowercase sentence:')

secuencia = SECUENCE_INIT

package = Paquete(EMISOR_PORT, RECEPTOR_PORT, data, secuencia)
message = dumps((receiver, package))

emisor.sendto(message, (NETWORK_IP, NETWORK_PORT))
timer = TIMEOUT
while timer >= 0:
    #ver en caso de perdido que no sea bloqueante la lectura de msjs de llegada
    incoming_message, serverAddress = emisor.recvfrom(LONGITUD_UDP)
    sender, incomming_package = loads(incoming_message)
    if timer == 0 or package.checksum != int(incomming_package.datos) or incomming_package.secuencia == secuencia:
        emisor.sendto(message, (NETWORK_IP, NETWORK_PORT))
        timer = TIMEOUT
        print("reenviado")
    else:
        print("Se entregó ok")
        #En caso de tener el emisor en bucle incrementar secuencia
        break
    sleep(1)
    timer -= 1



emisor.close()
