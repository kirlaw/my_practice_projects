#!/usr/bin/python3
# author eloise

from socket import *
import select
import sys
from time import ctime

HOST = 'ip'
PORT = 7788
ADDR = (HOST, PORT)
BUFSIZ = 1024

server_socket = socket(AF_INET, SOCK_STREAM)
# 重用对应地址和端口
server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

server_socket.bind(ADDR)
server_socket.listen(128)
# 非阻塞
server_socket.setblocking(False)

client_socket = None
temp_client = None

while True:
    try:
        temp_client, client_addr = server_socket.accept()
    except Exception as e:
        client_socket = temp_client
        if client_socket:
            client_socket.setblocking(False)
            try:
                text = client_socket.recv(BUFSIZ)
                if not text:
                    print("bye")
                    exit(0)
                print(text.decode('utf-8'))
            except Exception as e:
                pass
