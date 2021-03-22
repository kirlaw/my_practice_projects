#!/usr/bin/python3
# author eloise

from socket import *
import time
import struct

HOST = '192.168.239.128'
PORT = 7788
ADDR = (HOST, PORT)
BUFSIZ = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
time.sleep(1)
file_len = client_socket.recv(4)
file_name = client_socket.recv(struct.unpack('I', file_len)[0])
print(file_name.decode('utf-8'))
with open(file_name.decode('utf-8'), 'wb')as f:
    text_len = client_socket.recv(4)
    text = client_socket.recv(struct.unpack('I', text_len)[0])
    f.write(text)

client_socket.close()
