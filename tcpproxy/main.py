# -*- coding=utf-8 -*-
import threading
import socket

def main():
    port = 10500
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',port))
    s.listen(5)
    while True:
        aso, addr = s.accept()
        threading.Thread(target=connectTarget, args=(aso,)).start()
        print "%s has connected now." % addr[0]
    
def connectTarget(socket_in):
    target = "www.baidu.com"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((target,80))
    threading.Thread(target=do_proxy, args=(s, socket_in)).start()
    threading.Thread(target=do_proxy, args=(socket_in, s)).start()

def do_proxy(socket_in, socket_out):
    while True:
        rdata = None
        try:
            print "recieve data"
            rdata = socket_in.recv(1024)
        except Exception as e:
            print e
        if not rdata:
            try:
                addr, port = socket_out.getsockname()
                print "%s %s is closing." % (addr, port)
                socket_out.shutdown(socket.SHUT_WR)
                socket_out.close()
                socket_out = None
                print "%s %s closed" % (addr, port)
            except:
                print "socket_out already closed"
            break
        print "send data"
        socket_out.sendall(rdata)
        #print "%s ==> %s" % (socket_in.getsockname(), socket_out.getsockname())

   
    print "A Thread Exited!"
        
        
if __name__ == "__main__":
    main()