#!/usr/bin/env python
import os
import sys
import socket
import optparse
import random
import time
import json

def master():
    pid = os.getpid()
    return pid

master_pid = master()

def args():
    parser = optparse.OptionParser()
    parser.add_option('-p', '--processes', action="store", type="int", dest="procs")
    return parser

def count(n):
    c = 0
    start = time.time()
    while time.time() < start + n:
        c += 1
    return c

def fib(n):
    if n < 2:
        return n
    else:
        return fib(n-1) + fib(n-2)

def fact(n):
    if n < 2:
        return n
    else:
        return n * fact(n-1)


class Processes(object):
 
    # Processes object is instantiated with:
    # children - number of child processes
    # func - the job to execute
    # args - the function arguments
    def __init__(self, children, func, args):
        self.children = children
        self.func = func
        self.args = args
        self.results = []
        self.master = os.getpid()

    def run(self):
        for i in range(self.children):
            try:
                #while os.getpid() != self.master:
                start = time.time()
                child = os.fork()
                pid = os.getpid()
                with open('/etc/ipc/pids.txt', 'a') as f:
                    if pid != self.master:
                        f.write(str(pid)+'\n')
                
                
                #child = os.forkpty()

                if child != 0:
                    sys.exit(0)
                childsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host, port = open('/etc/ipc/sock.txt', 'r').read().split('\n')
                childsock.connect((host, int(port)))

                # execute the task
                result = self.func( *self.args )

                self.results.append( result )
                end = time.time() - start
                
                if child == 0:
                    #childsock.send("PID: {0}\nResult: {1}\nExecution time: {2}\n\n".format(child, result, end))
                    data = {'pid' : pid, 'data' : result}
                    childsock.send(json.dumps(data))
                elif child == self._master:
                    childsock.send("You are in the master")
                else:
                    childsock.send("Not in child process {0}".format(child))
                     
                sys.exit(0)

            except:
                continue 
  

    def get_children(self):
        pass

    def get_number(self):
        pass



if __name__ == '__main__':
    parser = args()
    parser = parser.parse_args(sys.argv[1:])[0]
    if parser.procs:
        #p = Processes(parser.procs, count, [20])
        p = Processes(parser.procs, fib, [10])
        p.run()
    else:
        print "Error: invalid arguments"
        sys.exit(1)
