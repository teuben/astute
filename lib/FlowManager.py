#! /usr/bin/env python
#
#  ADMIT2:  FlowManager
#
#  this managed ADMIT tasks and their flow
#
#
import sys, os, errno, fnmatch

_debug = False
_debug = True

# ==============================================================================

class FlowManager():
    """  Manages the flow of tasks
    """
    def __init__(self, name='none', project=None):

        self.connmap      = []        # list of (i1,j1,i2,j2) connections where i refers to task a[i], j to bdp[j]
        self.depsmap      = []        # processed list of dependencies
        self.tasks        = {}        # dictionary of tasks. The taskid (0,1,....) is the key
        self.changed_conn = True      # state if we got new connection map entries

    def __len__(self):
        return len(self.tasks)

    def __getitem__(self,index):
        return self.tasks[index]

    def makedepsmap(self):
        """ rebuild the connection map 
        """
        if True:
            # fake a depsmap before we know how to build it
            # this works as long as you added at's in the proper execution order
            # as scripts normally do
            self.depsmap = []
            for key in self.tasks:
                self.depsmap.append( [self.tasks[key].taskid] )

        self.change_conn = False

    def run(self):
        """ run all the tasks in the correct order 
        """
        if self.changed_conn: 
            self.makedepsmap()

        for dl in self.depsmap:
            # the dl[] are tasks that are independant, and could be run in parallel
            for d in dl:
                self.tasks[d].run()

    def add(self, a, lot = None):
        """Add an AT to the stack of AT's this ADMIT  contains
        self.depsmap = []     Also adjust the mapping 
        Usually all but the first task will have a lot (List of Tuples)
        """
        self.change_conn = True
        self.tasks[a.taskid] = a
        a.check()
        if len(a.bdp_in) != 0:
            print "WARNING WARNING: bdp_in not empty, not expected, probably an error"

        # loop over the List of Tuples
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
        print "=== FM: " 
        for cm in self.connmap:
            print "connmap",cm[0], cm[1],cm[2],cm[3]
            print "       ", self.tasks[cm[0]].name, self.tasks[cm[0]][cm[1]].filename,self.tasks[cm[2]].name
        for i in range(len(self.depsmap)):
            print "%d : %s" % (i,self.depsmap[i])
        for dl in self.depsmap:
            for d in dl:
                print "TASK %d: %s" % (d,self.tasks[d].name)
