import socket
import time

#host = '192.168.1.3' #vinay's GT IP
host = ''
port = 5052

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
resp = s.send('1')
print resp
resp = s.send('3')
print resp
