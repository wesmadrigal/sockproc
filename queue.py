#!/usr/bin/env python

"""
Queue class used to queue up arbitrary number
of tasks and arguments
"""


class Queue(object):
    def __init__(self, *args):
        self.tasks = {'tasks' : []}
        for arg in args:
            self.tasks['tasks'].append( arg )

    def __str__(self):
        return str(self.__class__)

    def __repr__(self):
        return str(self.__class__)

    def __del__(self):
        self.__init__()

    def get(self):
        return self.tasks['tasks'].pop()

    def put(self, task):
        self.tasks['tasks'].append( task ) 

    def get_breadth(self):
        task = self.tasks['tasks'][0]
        del self.tasks['tasks'][0]
        return task

    def set_manager(self, manager):
        self.manager = manager
