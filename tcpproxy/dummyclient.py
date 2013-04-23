# -*- coding=utf-8 -*-
import socket

HRequest = """GET / HTTP/1.1
Accept-Encoding: identity
Host: www.baidu.com
Connection: close
User-Agent: Python-urllib/2.7

"""

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('192.168.0.101',10500))
#s.connect(('www.baidu.com',80))
s.sendall(HRequest)
while True:
        data = s.recv(1024)
        if not data:
                break
        print data
s.close()