#!/usr/bin/env python
import socket
import os
import optparse
import sys
import json

# this program spawns a unix server socket for clients to connect to
# it then in turn spawns client sockets to communicate with the clients
# that have connected

def setup_parser():
    parser = optparse.OptionParser()
    parser.add_option('-H', '--host', type="string", dest="host")
    parser.add_option('-p', '--port', type="int", dest="port")
    parser.add_option('-l', '--limit', type="int", dest="limit")
    return parser

class MasterProcess(object):
    def __init__(self, host, port, limit=2, **kwargs):
        self._host = host
        self._port = port
        self._pid = os.getpid()
        self.children = limit
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.child_ids = []
        self.results = []
        
    def setup(self):
        self.sock.bind( (self._host, self._port) )
        self.sock.listen(self.children)
        with open('/etc/ipc/sock.txt', 'w') as f:
            f.write(self._host + '\n' + str(self._port))
    
    
    def handle_connections(self):
        while len(self.connections) < self.children:
            (child, addr) = self.sock.accept()
            self.connections.append(child)
            data = child.recv(10000)
            data = json.loads(data)
            self.child_ids.append(data['pid'])
            self.results.append(data['data'])
            print "Received child: {0}\Data: {1}".format(data['pid'], data['data'])

        self.tearDown()

    def tearDown(self):
        #for child_id in self.child_ids:
        #    os.system("kill -9 {0}".format(child_id))
        #    print "Killed id {0}".format(child_id)
        pids = open('/etc/ipc/pids.txt', 'r').read().split('\n')
        for i in pids:
            if i != '':
                os.system("kill -9 {0}".format(i))
        os.remove('/etc/ipc/pids.txt')
    
 
