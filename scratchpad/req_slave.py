import socket
import time

host = '192.168.1.2' #vinay's GT IP
port = 5002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
resp = s.send(1)
print resp
resp = s.send(3)
print resp
