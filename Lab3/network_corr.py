#!/usr/bin/env python
# encoding: utf-8
"""
network.py
"""
from paquete import *
from random import random, choice

def recv_pckt(socket):
	data, emisor = socket.recvfrom(1024)
	receptor, pckt = loads(data)
	return emisor, receptor, pckt

def send_pckt(socket, emisor, receptor, pckt):
	data = dumps((emisor, pckt))
	socket.sendto(data, receptor)

def process_pkt(pckt):
	addrs = (pckt)
	return pckt, addrs

def corrupt_packet(pckt):
	pckt.checksum 	= pckt.checksum + 20
	return pckt

def shut_down(socket, signal, frame):
	socket.close()
	exit(0)

def corruptNet(sock, sender, receiver, pckt):
	if (sender == (EMISOR_IP, EMISOR_PORT)):
		prob = choice([3,3,3,3,3,3,3,5])#int(random() * 10)
		if prob < 2:
			# Paquete Corrupto
			pckt = corrupt_packet(pckt)
			send_pckt(sock, sender, receiver, pckt)
			print("Corrupto")
		elif 2 <= prob and prob < 3:
			# Paquete duplicado
			send_pckt(sock, sender, receiver, pckt)
			send_pckt(sock, sender, receiver, pckt)
			print("Duplicado")
		elif 3 <= prob and prob < 4:
			# Paquete Perdido
			print("Perdido")
			return
		else:
			# Eventualmente mandamos el paquete
			send_pckt(sock, sender, receiver, pckt)
			print("Enviado")
	else:
		send_pckt(sock, sender, receiver, pckt)

if __name__ == "__main__":
	# Creamos el socket para la red
	sock = socket(AF_INET, SOCK_DGRAM)
	# Lo ligamos a su direccion
	sock.bind((NETWORK_IP, NETWORK_PORT))
	# Registramos la senial de salida
	signal.signal(signal.SIGINT, partial(shut_down, sock))
	# Imprimimos mensaje
	print('Red Habilitada')

	while True:
		sender, receiver, pckt = recv_pckt(sock)
		corruptNet(sock, sender, receiver, pckt)

