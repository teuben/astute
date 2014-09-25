#! /usr/bin/env python
#
#  ADMIT2:  AT centric version of ADMIT
#
#  simple container to put all of the ADMIT, BDP and AT in one file for testing
#
#  no 'import casa' or so allowed here. All package specific work needs to be delegated
#  If your AT_xxx needs casa routines, they need to be in a separate module
#
#
import sys, os, errno, fnmatch
import copy
import cPickle as pickle
import numpy as np
import parfile

_debug = False
_debug = True

# ==============================================================================

class FlowManager():
    projectid = 0
    def __init__(self, name='none', project=None):

        self.debug   = False
        self.connmap = []        # list of (i1,j1,i2,j2) connections where i refers to task a[i], j to bdp[j]
        self.depsmap = []
        self.tasks = {}

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self,index):
        return self.tasks[index]

    def add(self, a, lot = None):
        """Add an AT to the stack of AT's this ADMIT  contains
   self.depsmap = []     Also adjust the mapping 
        Usually all but the first task will have a lot (List of Tuples)
        """
        self.tasks[a.taskid] = a
        a.check()
        if len(a.bdp_in) != 0:
            print "WARNING WARNING: bdp_in not empty"
        if lot != None:
            for i in range(len(lot)):
                #print lot
                #print self.tasks
                st_id = lot[i][0]
                sb_id = lot[i][1]
                self.connmap.append( (st_id,sb_id,a.taskid,i) )
                #print st_id,sb_id,self.tasks[0]
                a.bdp_in.append( self.tasks[st_id][sb_id] )
        return a.taskid

    def get_conn(self):
        return self.connmap;

    def show(self):
        print "=== ADMIT(%s): %s" % (self.name, self.project)
        for cm in self.connmap:
            print "connmap",cm[0], cm[1],cm[2],cm[3]
            print "connmap", self.tasks[cm[0]].name, self.tasks[cm[0]][cm[1]].filename,self.tasks[cm[2]].name
 
