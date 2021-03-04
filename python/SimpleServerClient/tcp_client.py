#!/usr/bin/python3
# author eloise

from socket import *

HOST = '192.168.239.128'
PORT = 21567
ADDR = (HOST, PORT)
BUFSIZ = 1024

tcp_cs = socket(AF_INET, SOCK_STREAM)
tcp_cs.connect(ADDR)

data = input()
tcp_cs.send(data.encode('utf-8'))
data = tcp_cs.recv(BUFSIZ)
print(data.decode('utf-8'))

tcp_cs.close()
