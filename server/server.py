# Echo server program
import socket
import time

HOST = '0.0.0.0'                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    print 'Connected by', addr
    f = open('test.mp3','wb')
    while 1:
        l = conn.recv(1024)
        while l:
            f.write(l)
            l = conn.recv(1024)
    f.close()
    conn.close()
s.close()
