#!/usr/bin/python3
# author eloise

from socket import *
import select
import sys
import time

HOST = 'ip'
PORT = 7788
ADDR = (HOST, PORT)
BUFSIZ = 1024

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
client_socket.send(time.ctime().encode('utf-8'))
time.sleep(5)
client_socket.close()
