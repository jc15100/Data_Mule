import os
import time
worldSpins = True
pollDelaySecs = 0

nodes = [1,2,3,4,5]
nodeStatus = dict()

while(worldSpins):
#for i in range(5):
        for n in nodes:
                addrStr = '192.168.1.' + str(n)
                print 'Pinging:', addrStr
                status = os.system('ping -c 1 -w 1 ' + addrStr + ' &>/dev/null')
                if status != 0:
                        nodeStatus[n] = 0
                else:
                        nodeStatus[n] = 1
                time.sleep(pollDelaySecs)
                print nodeStatus
