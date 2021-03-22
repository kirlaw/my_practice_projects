#!/usr/bin/python3
# author eloise

from socket import *

HOST = 'ip'
PORT = 21567
ADDR = (HOST, PORT)
BUFSIZ = 1024

# 创建服务器套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)
# 绑定服务器套接字
udp_socket.bind(ADDR)

data = udp_socket.recvfrom(BUFSIZ)
print(data)
print(data[0].decode('utf-8'))
# print(data[1])  # 客户端的ip地址和端口，元组形式
udp_socket.sendto('i\'m fine thank u, and u'.encode('utf-8'), data[1])
data = udp_socket.recvfrom(BUFSIZ)
print(data[0].decode('utf-8'))

udp_socket.close()
