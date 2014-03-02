import socket
import os
import time

hellFrozenOver = False
headersFile = "mule_data.cmdb"

## interface stuff
if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])


def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1", 
            "wifi0",
            "ath0", 
            "ath1", 
            "ppp0", 
        ]
        for ifname in ['wlan0']: #used to be interfaces
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass 
    return ip
##

host = get_lan_ip()
port = int(host.split(".")[3]) + 10000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print "Opened socket at:", (host, port)

s.listen(1)

#We have INCOMING!
conn, addr = s.accept()

while not hellFrozenOver:
    reqId = conn.recv(1024)

    if reqId == 'ID':
        fh = open(os.path.expanduser("~")+"/mule/" + headersFile, 'rb')
        chunk = fh.read(1024)
        while(chunk):
            conn.send(chunk)
            chunk = fh.read(1024)

    else:
        #we assume this is just a file name
        f = open(os.path.expanduser("~")+"/mule/" + reqId, 'rb')
        chunk = f.read(1024)
        while(chunk):
            conn.send(chunk)
            chunk = f.read(1024)
