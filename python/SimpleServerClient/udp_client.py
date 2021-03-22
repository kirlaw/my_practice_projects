#!/usr/bin/python3
# author eloise

from socket import *

HOST = 'ip'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

udp_socket = socket(AF_INET, SOCK_DGRAM)

udp_socket.sendto(b'how are u', ADDR)
data = udp_socket.recvfrom(BUFSIZ)
udp_socket.sendto(b'i\'m fine too', ADDR)
print(data[0].decode('utf-8'))

udp_socket.close()
