# Echo client program
import socket

HOST = '0.0.0.0'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
f = open("opening.mp3", "rb") 
l = f.read(1024)
while(l):
    s.send(l)
    l = f.read(1024)
s.close()
print 'Received'#, repr(data)
