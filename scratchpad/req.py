import socket
import time

host = ''
port = 22580

one = 'One\r\n'
two = 'Two\r\n'
three = 'Three\r\n'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

while(True):
	reqId = conn.recv(1024)
	print 'Received:', reqId
   
	if reqId == '1':
		conn.send('one')
	elif reqId == '2':
		conn.send('two')
	elif reqId == '3':
		conn.send('three')
	else:
		conn.send('Git lost!')
		break
conn.close()


