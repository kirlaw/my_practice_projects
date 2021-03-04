#!/usr/bin/python3
# author eloise

from socket import *

HOST = '192.168.239.128'
PORT = 7788
ADDR = (HOST, PORT)
BUFSIZ = 1024

tcp_cs = socket(AF_INET, SOCK_STREAM)
tcp_cs.connect(ADDR)

data = input("输入想要下载的文件名：")
tcp_cs.send(data.encode('utf-8'))
data = tcp_cs.recv(BUFSIZ)
print(data.decode('utf-8'))

tcp_cs.close()
