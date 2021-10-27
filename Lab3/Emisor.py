import select
from time import sleep
from socket import *
from constantes import *
from paquete import Paquete


receiver = (RECEPTOR_IP, RECEPTOR_PORT)

emisor = socket(AF_INET, SOCK_DGRAM)
emisor.bind((EMISOR_IP, EMISOR_PORT))

timer = TIMEOUT
secuencia = SECUENCE_INIT % 2

last_sended = None

inputs = [emisor]
outputs = [emisor]
errors = []

while inputs:
    entradas, salidas, errores = select.select(inputs, outputs, errors, float(timer))

    # Timeout retorna tres listas vacías
    if entradas == [] and salidas == [] and errores == []:
        message = last_sended
        emisor.sendto(message, (NETWORK_IP, NETWORK_PORT))
        timer = TIMEOUT

    for input_signal in entradas:
        incoming_message, serverAddress = emisor.recvfrom(LONGITUD_UDP)
        sender, incomming_package = loads(incoming_message)

        if incomming_package.secuencia == secuencia:
            message = last_sended
            emisor.sendto(message, (NETWORK_IP, NETWORK_PORT))
            timer = TIMEOUT
        else:
            print(package.datos)
            secuencia = (incomming_package.secuencia + 1) % 2


    for output in outputs:

        if last_sended == None or loads(last_sended)[1].secuencia != secuencia:
            data = input('Input lowercase sentence:')

            package = Paquete(EMISOR_PORT, RECEPTOR_PORT, data, secuencia)
            message = dumps((receiver, package))

            emisor.sendto(message, (NETWORK_IP, NETWORK_PORT))
            last_sended = message
            timer = TIMEOUT
        sleep(1)
        if timer != 0:
            timer -= 1

