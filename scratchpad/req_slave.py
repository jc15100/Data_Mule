import socket
import time

#host = '192.168.1.3' #vinay's GT IP
host = '143.215.51.230' 
port = 10230

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

#s.send('ID')
#resp = s.recv(1024)
#print resp

s.send('watson')
resp = s.recv(1024)
print resp


