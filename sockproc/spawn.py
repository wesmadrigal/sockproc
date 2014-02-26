#!/usr/bin/env python
import os
import sys
import socket
import optparse
import random
import time
import json



class Pool(object):
    # Processes object is instantiated with:
    # children - number of child processes
    # func - the job to execute
    # args - the function arguments
    def __init__(self, children, func, args):
        self.children = children
        self.func = func
        self.args = args
        self.results = []
        self.child_socks = []
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
                    continue
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
                     
                # kill yourself
                os.system("kill -9 {0}".format(pid))

            except:
                continue 
  

    def get_child_socks(self):
        return self.child_socks

    def process_count(self):
        return self.children



class Process(object):
    def __init__(self, func, args, parent_pid=None):
        self._func = func
        self._args = args
        self._heartstart = None
        self._heartstop = None
        self._alive = False
        self._pid = None
        self._parent_pid = parent_pid
        self._result = None
        
    def __str__(self):
        return str(self.__class__)

    def __del__(self):
        if self._pid is not None and self._pid != self._parent_pid:
            os.system("kill -9 {0}".format(self._pid))

    def start(self):
        self._heartstart = int(time.time())
        self._alive = True

    def stop(self):
        self._heartstop = int(time.time())
        self._alive = False

    def run_async(self):
        self.start()
        try:
            #import pdb
            #pdb.set_trace()
            start = time.time()
            child = os.fork()

            if child == 0:
                self._pid = os.getpid()
                with open('/etc/ipc/pids.txt', 'a') as f:
                    if self._pid != self._parent_pid:
                        f.write(str(self._pid)+'\n')
                
                if self._parent_pid is not None:
                    self.connect()
                # execute the task
                result = self._func( *self._args )

                self.result = result

                self.execution_time = time.time() - start
    
                if hasattr(self, '_sock'):            
                    if child == 0:
                        data = {'pid' : self._pid, 'data' : self.result}
                        self._sock.send(json.dumps(data))
                    elif child == self._master:
                        self._sock.send("You are in the master")
                    else:
                        self._sock.send("Not in child process {0}".format(child))
                    
                self.cleanup()

            else:
                pass

        except:
            class ProcessError(Exception):
                def __init__(self):
                    super(ProcessError, self).__init__()

            self.cleanup()

            raise ProcessError

    def run(self):
        self.start()
        start = time.time()
        self.result = self._func(*self._args)
        self.execution_time = time.time() - start
         

    def connect(self):
        if not hasattr(self, '_sock'):
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = open('/etc/ipc/sock.txt', 'r').read().split('\n')
            self._sock.connect((host, int(port)))
 
    def cleanup(self):
        if self._pid is not None:
            os.system("kill -9 {0}".format(self._pid))

    def get_result(self):
        return self._result

   

 
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
