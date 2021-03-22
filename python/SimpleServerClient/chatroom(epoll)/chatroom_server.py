#!/usr/bin/python3
# author eloise

from socket import *
import select
import sys
from time import ctime

HOST = '172.17.151.9'
PORT = 7788
ADDR = (HOST, PORT)
BUFSIZ = 1024

tcp_ss = socket(AF_INET, SOCK_STREAM)
tcp_ss.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcp_ss.bind(ADDR)
tcp_ss.listen(128)

epoll = select.epoll()
epoll.register(tcp_ss.fileno(), select.EPOLLIN)
# 存放聊天室用户的cs信息
client_list = []
# 存放用户名
client_name = {}

while True:
    epoll_list = epoll.poll()
    for fd, event in epoll_list:
        if fd == tcp_ss.fileno():
            tcp_cs, client_addr = tcp_ss.accept()
            name = tcp_cs.recv(BUFSIZ).decode('utf-8')
            # 登记用户
            client_name[tcp_cs] = name
            client_list.append(tcp_cs)
            print("[{}]{} is coming".format(ctime(), client_name[tcp_cs]))
            print("现在聊天室有%d个用户" % len(client_list))
            epoll.register(tcp_cs.fileno(), select.EPOLLIN)
        for client in client_list:
            if fd == client.fileno():
                # 读取数据，群发
                recv_data = client.recv(BUFSIZ)
                # 若未响应，删除用户
                if not recv_data:
                    epoll.unregister(client.fileno())
                    client_list.remove(client)
                    print('{}退出聊天室'.format(client_name[client]))
                    del client_name[client]
                    print("现在聊天室有%d个用户" % len(client_list))
                    client.close()
                else:
                    for other_client in client_list:
                        if other_client is not client:
                            other_client.send(recv_data)

tcp_cs.close()

tcp_ss.close()
