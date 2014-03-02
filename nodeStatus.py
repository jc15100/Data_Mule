import os
import time

nodes = [1,2,3,4,5]
IPprefix = '192.168.1.'
portBase = 5000

worldSpins = True
pollDelaySecs = 0

nodeStatus = dict()
metRecently = dict()

while(worldSpins):
#for i in range(5):
        for n in nodes:
                addrStr = IPprefix + str(n)
                print 'Pinging:', addrStr
                status = os.system('ping -c 1 -w 1 ' + addrStr + ' &>/dev/null')
                if status != 0:
                        isNodeHere[n] = False
                else:
                        isNodeHere[n] = True
                time.sleep(pollDelaySecs)
                print nodeStatus

		newNodes = [node for node in isNodeHere.keys() if metRecently[node] != True]
		for node in newNodes:
			#ping again, just to be sure
			status = os.system('ping -c 1 -w 1 ' + addrStr + ' &>/dev/null')
			
                        if status != 0:
                                #set up socket
                                host = IPprefix + str(node)
                                port = portBase + node
                                #send 'IDs'
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.connect((host, port))
                                s.send('ID')
                                lstHeaders = s.recv(1024)
                                #compare IDs
                                #open header files, do a comparison between lstHeaders and the stuff read off the disk
                                
                                #send (host, port) 
				metRecently[node] = True
			else:
				#he's gone.
				isNodeHere[node] = False

