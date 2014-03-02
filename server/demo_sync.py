#!/usr/bin/env python

__author__ = 'Andrew Price'

#import pickle
import cPickle as pickle
import os.path
import socket
import SocketServer


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
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


class MuleRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)

    def setup(self):
        return SocketServer.BaseRequestHandler.setup(self)

    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        print "Server got message:", data
        self.request.send(data)
        return

    def finish(self):
        return SocketServer.BaseRequestHandler.finish(self)



class RemoteNode:

    def __init__(self, ip_address):
        # Do nothing
        self.ip_address = ip_address

    def get_ids(self):
        return set(["cat", "dog"]), set(["bird", "fish"])

    def request_for_ids(self, requested_ids):
        return dict()


class DataStore:

    def __init__(self, filename="/home/arprice/mule/mule_data.cmdb"): #"/temp/mule_data"):
        self.file_id = filename
        self.pending_data = dict()
        self.completed_ids = set()
        if os.path.isfile(self.file_id):
            with open(self.file_id, "rb") as f:
                self.pending_data, self.completed_ids = pickle.load(f)
        else:
            print "File store does not exist yet."

    def fake_data(self):
        self.pending_data = dict([("cat", 5), ("bird", 3), ("fish", 1), ("horse", 2)])

    def found_neighbor(self, node):
        neighbor_completed, neighbor_pending = node.get_ids()
        #neighbor_completed = set()
        #neighbor_pending = set()

        # Update list of completed IDs
        self.completed_ids.update(neighbor_completed)

        # Delete any pending entries that have been completed
        for k in self.pending_data.keys():
            if k in self.completed_ids:
                del self.pending_data[k]

        # Get list of any needed updates
        needed_ids = set(self.pending_data.keys()).difference(neighbor_pending)

        # Get the neighbor's pending data
        neighbor_data = node.request_for_ids(needed_ids)
        self.pending_data.update(neighbor_data)

        # Save the data to the file store
        with open(self.file_id, "w+") as f:
            pickle.dump((self.pending_data, self.completed_ids), f)


def test_server():
    addr = get_lan_ip()
    port_num = int(addr.split(".")[3]) + 10000
    print "Spinning up Mule server:", addr + ":" + str(port_num)
    address = (addr, port_num)
    server = SocketServer.TCPServer(address, MuleRequestHandler)
    print "Server Address:", server.server_address

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    print "Socket Connected"
    len_sent = s.send("Hello World")
    print "Request sent"
    response = s.recv(len_sent)
    print "Response:", response

    s.close()

    server.socket.close()

if __name__ == "__main__":
    ds = DataStore()
    ds.fake_data()

    rn = RemoteNode("192.168.1.1")

    ds.found_neighbor(rn)

    print "Completed:", ds.completed_ids
    print "Pending:", ds.pending_data.keys()

    test_server()