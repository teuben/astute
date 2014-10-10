#! /usr/bin/env python
#
#  ADMIT Flow Manager
#
#  Manages ADMIT tasks and flow
#
#

import sys, os, errno, fnmatch

_debug = False
_debug = True

# ==============================================================================

class FlowManager():
    """  Manages the flow of tasks
    """
    def __init__(self):

        self.connmap = []         # list of (i1,j1,i2,j2) connections
                                  # where i1 is source task: a[i1]; j1 is source output bdp: bdp[j1];
                                  # i2 is destination task: at[i2]; j2 is destination input bdp[j2]

        self.depsmap = []         # list of lists of tasks at the same dependency level
                                  # example: [ [a1, a2], [a3, a4, a5] ]
                                  #          level 0: a1, a2
                                  #          level 1: a3, a4, a5

        self.tasks = {}           # dictionary of tasks. The task-id (0,1,....) is the key
        self.changed_conn = True  # state if we added new connection entries

    # return length of tasks
    def __len__(self):
        return len(self.tasks)

    # return one task
    def __getitem__(self, index):
        return self.tasks[index]

    def makedepsmap(self):
        """ make dependency map from connection map """

#         if True:
#             # fake a depsmap before we know how to build it
#             # this works as long as you added at's in the proper execution order
#             # as scripts normally do
#             self.depsmap = []
#             for key in self.tasks:
#                 self.depsmap.append( [self.tasks[key].taskid] )

        tmp_cmap = list(self.connmap)
        task_ids = self.tasks.keys()

        num = len(tmp_cmap)

        # we only loop through the connection map at most num times (worst case: only one task at each level)
        # to prevent getting in an infinite loop if the connection map is not a good one
        while num > 0 and len(tmp_cmap) > 0 :
            num = num - 1
            roots = []
            roots = self.findroot(tmp_cmap)
            print num

            if len(roots) > 0 :
                same_level = []
                for node in roots:
                    at = node[0]  # source task
 
                    # now check if this task is already in the list
                    found = False
                    if len(same_level) > 0:
                        for t in same_level:
                            if at == t :
                                found = True
                                pass

                    # add this task to the same dependent level list
                    if not found:
                        same_level.append(at)
                        task_ids.remove(at)  ## the last task would be the leaf node at the bottom

                    tmp_cmap.remove(node)  ## remove the root node from the connection map

                self.depsmap.append( same_level )

        # add the last task to the dependency map
        self.depsmap.append(task_ids)
        self.change_conn = False

    def run(self):
        """ run all the tasks in the correct order 
        """
        if self.changed_conn: 
            self.makedepsmap()

        for dl in self.depsmap:
            # the dl[] are tasks that are independent, and could be run in parallel
            for d in dl:
                self.tasks[d].run()

    def add(self, a, tuples = None):
        """Add an AT to the task list
           Usually all but the first task will have a List of Tuples (each tuple = (source at, source bdp)).
           The tuples came in with this task are the sources.
        """
        self.change_conn = True
        self.tasks[a.taskid] = a
        # a.check()
        if len(a.bdp_in) != 0:
            print "WARNING WARNING: bdp_in not empty, not expected, probably an error"

        # loop over the List of Tuples
        if tuples != None:
            for i in range(len(tuples)):
                source_at_id = tuples[i][0]
                source_bdp_id = tuples[i][1]
                self.connmap.append( (source_at_id, source_bdp_id, a.taskid, i) )

                # now the bdp input of this task comes from source bdp
                a.bdp_in.append( self.tasks[source_at_id][source_bdp_id] )

        return a.taskid

    def get_conn(self):
        return self.connmap;

    def show(self):
        print "=== FM: connection map", self.connmap
        print "=== FM: tasks ======="
        for key in self.tasks:
            print key, ":", self.tasks[key].taskid, self.tasks[key].name
        print "=== FM: dependency map", self.depsmap
        for cm in self.connmap:
            print "connmap", cm[0], cm[1], cm[2], cm[3]
            # print "       ", self.tasks[cm[0]].name, self.tasks[cm[0]][cm[1]].filename,self.tasks[cm[2]].name
            print "src task:", self.tasks[cm[0]].name
            print "bdp out:", self.tasks[cm[0]][cm[1]].filename
            print "des task:", self.tasks[cm[2]].name
            # print "bdp in:", self.tasks[cm[0]][cm[3]].filename  ## commented out because the following error:
                                                                  ## admit2.py", line 441, in __getitem__
                                                                  ## return self.bdp_out[index]
                                                                  ## IndexError: list index out of range

            print
        for i in range(len(self.depsmap)):
            print "%d : %s" % (i,self.depsmap[i])
        for dl in self.depsmap:
            for d in dl:
                print "TASK %d: %s" % (d,self.tasks[d].name)

    def verify(self):
#         tmp_cmap = copy.deepcopy(self.connmap)
        tmp_cmap = list(self.connmap)
        num = len(tmp_cmap)

        # we only check the nodes num of times to prevent getting in an infinite loop
        while num > 0 and len(tmp_cmap) > 0 :
            roots = []
            roots = self.findroot(tmp_cmap)
            print num
            if len(roots) > 0 :
                for node in roots:
                    tmp_cmap.remove(node)  ## remove the root nodes

            num = num -1

        if len(tmp_cmap) != 0:    ## no root found - this connection map is not valid
            return False
        else:
            return True
            
    def findroot(self, cmap=None):
        if cmap == None:
            cmap = self.connmap

        roots = []
        src_index = 0
        des_index = 2

        for cm in cmap:
            isroot = True

            # first check if this connection node points to itself
            if cm[src_index] == cm[des_index]:
                print "Self loop found:", cm
                return roots

            for cm2 in cmap:
                if cm[src_index] == cm2[des_index]:
                    # if the source task is found within destination tasks, then it is not a root
                    isroot = False
                    pass

            if isroot:
                print "root connection node:", cm
                roots.append(cm)

        return roots


    def test_flow4(self):
        self.connmap = [(0, 0, 1, 0), (0, 0, 2, 0), (1, 0, 3, 0), (2, 0, 3, 1)]
        self.connmap = [("a0", 0, "a1", 0), ("a0", 0, "a2", 0), ("a1", 0, "a3", 0),("a2", 0, "a3", 1)]
        self.connmap = [("a0", 0, "a1", 0), ("a0", 0, "a2", 0), ("a1", 0, "a3", 0),("a2", 0, "a3", 1),("a3", 0, "a1", 1) ]
        print self.connmap;

# fm = FlowManager()
# fm.test_flow4()
# f = fm.findroot()
# if len(f) > 0:
#     print f
#     for node in f:
#         print node
#         print node[0]
# v = fm.verify()
# d = fm.makedepsmap()

