#!/usr/bin/python3
# author eloise

from socket import *
import sys

HOST = '192.168.239.128'
BUFSIZ = 1024


# 获取文件内容
def get_file_content(file_name):
    try:
        with open(file_name, 'rb') as f:
            t = f.read()
        return t
    except:
        print("文件%s不存在" % file_name)


def main():
    if len(sys.argv) != 2:
        print("请按照如下方式运行：python3 xxx.py 7788")
        return
    else:
        # 运行方式为python3 xxx.py 7788
        port = int(sys.argv[1])

    tcp_ss = socket(AF_INET, SOCK_STREAM)
    ADDR = (HOST, port)
    tcp_ss.bind(ADDR)
    tcp_ss.listen(128)

    while True:
        # 等待客户端连接
        tcp_cs, addr = tcp_ss.accept()
        data = tcp_cs.recv(BUFSIZ)
        file_name = data.decode('utf-8')
        print('要下载的文件为%s' % file_name)
        file_content = get_file_content(file_name)
        # 如果文件存在
        if file_content:
            tcp_cs.send(file_content)
        tcp_cs.close()

    tcp.ss.close()


if __name__ == "__main__":
    main()
