# -*- coding=utf-8 -*-

import select
import socket

proxypairs = {}

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('',10500))
serversocket.listen(5)
serversocket.setblocking(0)

epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
target = 'www.baidu.com'

try:
    conns = {}
    indata = {}
    while True:
        events = epoll.poll(1)
        for fileno, event in events:
            if fileno == serversocket.fileno():
                cconnection, address = serversocket.accept()
                cconnection.setblocking(0)
                epoll.register(cconnection.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLHUP)
                conns[cconnection.fileno()] = cconnection
                rconnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                rconnection.connect((target,80))
                rconnection.setblocking(0)
                epoll.register(rconnection.fileno(), select.EPOLLIN | select.EPOLLOUT | select.EPOLLHUP)
                conns[rconnection.fileno()] = rconnection
                proxypairs[rconnection.fileno()] = cconnection.fileno()
                proxypairs[cconnection.fileno()] = rconnection.fileno()
                indata[rconnection.fileno()] = ''
                indata[cconnection.fileno()] = ''
                continue
            elif event & select.EPOLLIN:
                abuff = conns[fileno].recv(1024)
                if abuff == '':
                    conns[proxypairs[fileno]].shutdown(socket.SHUT_WR)
                    epoll.unregister(fileno)
                    conns[fileno].close()
                    del conns[fileno], indata[fileno], proxypairs[fileno]
                    print fileno
                    continue
                indata[fileno] += abuff
            elif event & select.EPOLLOUT:
                try:
                    if indata[proxypairs[fileno]] == '':
                        continue
                except:
                    conns[fileno].shutdown(socket.SHUT_RDWR)
                    epoll.unregister(fileno)
                    conns[fileno].close()
                    del conns[fileno], indata[fileno], proxypairs[fileno]
                    print fileno
                    continue                    
                bw = conns[fileno].send(indata[proxypairs[fileno]])
                indata[proxypairs[fileno]] = indata[proxypairs[fileno]][bw:]
            elif event & select.EPOLLHUP:
                print "unregister %d" % fileno
                epoll.unregister(fileno)
                conns[fileno].close()
                del conns[fileno], indata[fileno], proxypairs[fileno]
            else:
                print event
finally:
    epoll.unregister(serversocket.fileno())
    epoll.close()
    serversocket.close()