import socket
import time

#host = '192.168.1.3' #vinay's GT IP
host = '127.0.0.1'
port = 22580

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

s.send('1')
resp = s.recv(1024)
print resp

s.send('2')
resp = s.recv(1024)
print resp

s.send('6\r\n')
resp = s.recv(1024)
print resp
