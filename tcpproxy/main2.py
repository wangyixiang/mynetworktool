# -*- coding=utf-8 -*-
#只是用来证明确实在python的封装的socket中的close并没有实际的关闭socket的代码
import threading
import _socket

def main():
    port = 10500
    s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    s.bind(('',port))
    s.listen(5)
    while True:
        aso, addr = s.accept()
        threading.Thread(target=connectTarget, args=(aso,)).start()
        print "%s has connected now." % addr[0]
    
def connectTarget(socket_in):
    target = "www.baidu.com"
    s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
    s.connect((target,80))
    threading.Thread(target=do_proxy, args=(s, socket_in)).start()
    threading.Thread(target=do_proxy, args=(socket_in, s)).start()

def do_proxy(socket_in, socket_out):
    while True:
        rdata = None
        try:
            print "recieve data"
            rdata = socket_in.recv(10240)
        except Exception as e:
            print e
        if not rdata:
            try:
                addr, port = socket_out.getsockname()
                print "%s %s is closing." % (addr, port)
                #socket_out.shutdown(_socket.SHUT_WR)
                socket_out.close()
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