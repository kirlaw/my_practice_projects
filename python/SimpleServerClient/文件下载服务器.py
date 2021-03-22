#!/usr/bin/python3
# author eloise

from socket import *
import struct, os
import time

HOST = 'ip'
PORT = 7788
ADDR = (HOST, PORT)
BUFSIZ = 1024

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server_socket.bind(ADDR)
server_socket.listen(128)
client_socket, client_addr = server_socket.accept()
print("连上了{}".format(client_addr))

file_name = 'readme.md'.encode('utf-8')
# 先发报文头
client_socket.send(struct.pack("I", len(file_name)))
client_socket.send(file_name)

# 文件内容
with open(file_name, 'rb') as f:
    text = f.read()
    client_socket.send(struct.pack('I', len(text)))
    client_socket.send(text)

time.sleep(5)
client_socket.close()
server_socket.close()
