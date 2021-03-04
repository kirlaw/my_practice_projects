#!/usr/bin/python3
# author eloise

from socket import *

HOST = '192.168.239.128'
PORT = 21567
ADDR = (HOST, PORT)
BUFSIZ = 1024

tcp_ss = socket(AF_INET, SOCK_STREAM)
tcp_ss.bind(ADDR)
# 监听连接 参数是连接被转接或拒绝之前，传入连接请求的最大数
tcp_ss.listen(5)
tcp_cs, addr = tcp_ss.accept()
print(addr)
data = tcp_cs.recv(BUFSIZ)
print(data.decode('utf-8'))
tcp_cs.send("吃了".encode('utf-8'))
tcp_cs.close()
tcp_ss.close()
