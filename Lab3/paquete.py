import math
from constantes import *

class Paquete:
    # Esta clase abstrae la definicion de un paquete empleado
    # por la red a utilizar. Los datos deben de viajar dentro
    # de los mismos y no sueltos.
    def __init__(self, pOrigen, pDestino, datos, secuencia):
        self.pOrigen    = pOrigen
        self.pDestino   = pDestino
        self.longitud   = len(datos)
        self.datos      = datos
        self.secuencia  = secuencia
        self.checksum   = calculo_checksum(self)

    @property
    def pOrigen(self):
        return self._pOrigen

    @pOrigen.setter
    def pOrigen(self, value):
        self._pOrigen = value

    @property
    def pDestino(self):
        return self._pDestino
    
    @pDestino.setter
    def pDestino(self, value):
        self._pDestino = value

    @property
    def checksum(self):
        return self._checksum

    @checksum.setter
    def checksum(self, value):
        self._checksum = value

    @property
    def longitud(self):
        return self._longitud
        
    @longitud.setter
    def longitud(self, value):
        if(value > LONGITUD_UDP):
            raise ValueError("La longitud del paquete supera lo soportado")
        self._longitud = value

    @property
    def datos(self):
        return self._datos

    @datos.setter
    def datos(self, value):
        self._datos = value

    @property
    def secuencia(self):
        return self._secuencia

    @secuencia.setter
    def secuencia(self, value):
        self._secuencia = value


def complemento_uno(number):
    num_bits = int(math.log2(number)) + 1
    complemento = ((0b1 << num_bits) - 1) ^ number
    return complemento


def calculo_checksum(packet):
    sum_aux = packet.pOrigen + packet.pDestino 
    sum_aux += packet.secuencia 
    sum_aux += packet.longitud
    sum_aux += packet.checksum if hasattr(packet, 'checksum') else 0
    resultado = complemento_uno(sum_aux)
    return resultado
