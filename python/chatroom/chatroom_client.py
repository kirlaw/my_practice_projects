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

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect(ADDR)

client_name = input("请输入用户名：")
client_socket.send(client_name.encode('utf-8'))

# 创建epoll对象
epoll = select.epoll()

# 设置监听对象
epoll.register(client_socket.fileno(), select.EPOLLIN)
epoll.register(sys.stdin.fileno(), select.EPOLLIN)

while True:
    epoll_list = epoll.poll()
    for fd, event in epoll_list:
        # 收到发送的信息
        if fd == client_socket.fileno():
            recv_data = client_socket.recv(BUFSIZ)
            if not recv_data:
                print("[{}]再见".format(ctime()))
                # 无错误退出
                exit(0)
            print('[{}]{}'.format(ctime(), recv_data.decode('utf-8')))
        # 缓冲区里有数据
        if fd == sys.stdin.fileno() and event == select.EPOLLIN:
            input_data = input()
            if not input_data:
                print("[{}]要走了".format(ctime()))
                exit(0)
            send_data = (client_name + ': ' + input_data).encode('utf-8')
            client_socket.send(send_data)

client_socket.close()
