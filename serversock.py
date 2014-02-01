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
    


# a method to handle the incoming serversocket connections and manage them
# n is the number of connections this particular serversocket can handle
def handle_connections(serversocket, n):
    connections = []
    while len(connections) < n:
        (client, addr) = serversocket.accept()
        connections.append(client)
        data = client.recv(10000)
        print data
        
    sys.exit(0)
    
 


if __name__ == '__main__':
    parser = setup_parser()
    parser = parser.parse_args(sys.argv[1:])[0]
    if not hasattr(parser, 'host') and not hasattr(parser, 'port'):
        sys.exit(1)
    else:
        #serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #serversocket.bind( (parser.host, parser.port) )
        master = MasterProcess( parser.host, parser.port )
        f = open('sock.txt', 'w')
        f.write(parser.host + '\n' + str(parser.port))
        f.close()
        master.setup()
        master.handle_connections() 
