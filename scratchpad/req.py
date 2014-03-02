import socket
import time

host = ''
port = 5052

one = 'One'
two = 'Two'
three = 'Three'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

while(True):
	conn, addr = s.accept()
	print 'Incoming request from:', addr

	reqId = conn.recv(1024)
	print 'Received:', reqId
	conn.close()
    
	if reqId == '1':
		s.send(one)
	elif reqId == '2':
		s.send(two)
	elif reqId == '3':
		s.send(three)


