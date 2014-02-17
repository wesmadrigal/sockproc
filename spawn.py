#!/usr/bin/env python
import os
import sys
import socket
import optparse
import random
import time
import json



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
                start = time.time()
                child = os.fork()
                pid = os.getpid()
                with open('/etc/ipc/pids.txt', 'a') as f:
                    if pid != self.master:
                        f.write(str(pid)+'\n')
                
                
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


