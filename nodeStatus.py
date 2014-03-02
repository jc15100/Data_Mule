import os
import time

nodes = [1,2,3,4,5]

worldSpins = True
pollDelaySecs = 0

nodeStatus = dict()
metRecently = dict()

while(worldSpins):
#for i in range(5):
        for n in nodes:
                addrStr = '192.168.1.' + str(n)
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
                                #send 'IDs'
                                #compare IDs
                                #send get(ID[i])
				metRecently[node] = True
			else:
				#he's gone.
				isNodeHere[node] = False

