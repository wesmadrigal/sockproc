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
    def __init__(self, host, port, children=2, **kwargs):
        self._host = host
        self._port = port
        self._pid = os.getpid()
        self.children = children
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.child_ids = []
        self.results = []
       
    def __repr__(self):
        return ' '.join([str(self.__class__), 'pid: {0}'.format(self._pid), 'children: {0}'.format(self.children)])

    def setup(self):
        self.sock.bind( (self._host, self._port) )
        self.sock.listen(self.children)
        with open('/etc/ipc/sock.txt', 'w') as f:
            f.write(self._host + '\n' + str(self._port))
    
    
    def handle_processes(self):
        # fork off a process and do the work
        
        os.system("> /etc/ipc/pids.txt")
        self.execute_handle()

        self.tearDown()        

    def execute_handle(self):
        while len(self.connections) < self.children:
            (child, addr) = self.sock.accept()
            self.connections.append( (child, addr) )
                                 
            data = child.recv(10000)
            data = json.loads(data)
            self.child_ids.append(data['pid'])
            self.results.append(data['data'])
            print "Received child: {0}\Data: {1}".format(data['pid'], data['data'])


    def tearDown(self):
        try:
            pids = open('/etc/ipc/pids.txt', 'r').read().split('\n')
            for i in pids:
                if i != '':
                    os.system("kill -9 {0}".format(i))
            os.remove('/etc/ipc/pids.txt')
        except IOError:
            print sys.exc_info()
    

    def get_id(self):
        return self._pid


    def reload(self, children=None):
        self.child_ids = []
        self.results = []
        self.connections = []
        if not children:
            self.sock.listen( self.children ) 
        else:
            self.sock.listen( children )
