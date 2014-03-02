#!/usr/bin/env python

__author__ = 'Andrew Price'

#import pickle
import cPickle as pickle
import os.path
import time
import socket
import urllib2
from uploadToAWS import CloudUploader


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


class NodeScanner:

    def __init__(self):
        self.nodes = [1, 2, 3, 4, 5]
        self.ip_prefix = '192.168.1.'
        self.port_base = 10000
        self.inner_poll_delay = 0
        self.outer_poll_delay = 5

        self.node_active = set()
        self.met_recently = set()

    def scan(self):
        for n in self.nodes:
            address_str = self.ip_prefix + str(n)
            print 'Pinging:', address_str
            status = os.system('ping -c 1 -w 1 ' + address_str)# + ' &>/dev/null')

            print status
            if status == 0:
                self.node_active.add(n)
                print "Found", n
            time.sleep(self.inner_poll_delay)

        #new_nodes = [node for node in self.node_active.keys() if self.met_recently[node] is not True]
        new_nodes = self.node_active - self.met_recently
        #self.met_recently = self.node_active

        return new_nodes

    def make_endpoint(self, num):
        return self.ip_prefix + str(num), self.port_base + num

    def check_internet_connection(self):
        try:
            response=urllib2.urlopen('http://www.google.com',timeout=1)
            return True
        except urllib2.URLError as err: pass
        return False


class RemoteNodeInterface:

    def __init__(self, (ip_address, port_num)):
        # Do nothing
        self.ip_address = ip_address
        self.port_num = port_num

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(1)
        try:
            self.socket.connect((self.ip_address, self.port_num))
            self.is_connected = True
        except Exception:
            print "Failed to connect to ", (self.ip_address, self.port_num)
            self.is_connected = False

    def read_socket_to_eof(self):
        if not self.is_connected:
            return ""

        # Read while there's data
        read_success = True
        data_string = ""
        while read_success:
            try:
                data_string += self.socket.recv(1024)
            except Exception:
                read_success = False
        return data_string

    def get_ids(self):
        if not self.is_connected:
            return set(), set()
        # Request the ID Stream
        self.socket.send('ID')

        # Get the serialized python set of keys
        data_string = self.read_socket_to_eof()

        # De-serialize into our set object
        neighbor_pending, neighbor_completed = pickle.loads(data_string)

        return neighbor_pending, neighbor_completed

    def test_get_ids(self):
        return set(["cat", "dog"]), set(["bird", "fish"])

    def request_data_for_ids(self, requested_ids, file_path):
        if not self.is_connected:
            return set()
        # Set to hold successful transfers
        success_ids = set()

        # Request the data file
        for rid in requested_ids:
            self.socket.send(rid)

            # Get the stream of data for the file
            data_string = self.read_socket_to_eof()

            with open(file_path + "/" + rid, "wb+") as f:
                f.write(data_string)

            success_ids.add(rid)

        return success_ids


class MuleDataStore:

    def __init__(self, file_path=os.path.expanduser("~")+"/mule_data"):
        self.file_id = file_path + "/mule_data.cmdb"
        self.directory = file_path
        self.pending_data = set()
        self.completed_ids = set()
        self.uploader = CloudUploader()
        if os.path.isfile(self.file_id):
            with open(self.file_id, "rb") as f:
                self.pending_data, self.completed_ids = pickle.load(f)
        else:
            print "File store does not exist yet."

    def fake_data(self):
        self.pending_data = dict([("cat", 5), ("bird", 3), ("fish", 1), ("horse", 2)])

    def found_neighbor(self, node):
        neighbor_pending, neighbor_completed = node.get_ids()
        #neighbor_completed = set()
        #neighbor_pending = set()

        print neighbor_pending, neighbor_completed

        # Update list of completed IDs
        self.completed_ids.update(neighbor_completed)

        # Delete any pending entries that have been completed
        for k in self.pending_data:
            if k in self.completed_ids:
                del self.pending_data[k]
                # Remove files?

        # Get list of any needed updates
        needed_ids = neighbor_pending - self.pending_data
        print "Need:", needed_ids

        # Get the neighbor's pending data
        got_ids = node.request_data_for_ids(needed_ids, self.directory)
        self.pending_data.update(got_ids)

        # Save the data to the file store
        with open(self.file_id, "w+") as f:
            pickle.dump((self.pending_data, self.completed_ids), f)
        # Upload to the cloud if there is pending data and an available internet connection
        if NodeScanner.check_internet_connection(self):
            if len(self.pending_data) > 0:
                self.uploader.upload(self.file_id)




def test_server():
    addr = get_lan_ip()
    port_num = int(addr.split(".")[3]) + 10000
    print "Spinning up Mule server:", addr + ":" + str(port_num)
    address = (addr, port_num)

if __name__ == "__main__":
    ds = MuleDataStore()
    ns = NodeScanner()

    while True:
        nodes = ns.scan()
        print "Scan Completed.", nodes
        for node in nodes:
            rn = RemoteNodeInterface(ns.make_endpoint(node))

            ds.found_neighbor(rn)

            print "Completed:", ds.completed_ids
            print "Pending:", ds.pending_data

        time.sleep(ns.outer_poll_delay)