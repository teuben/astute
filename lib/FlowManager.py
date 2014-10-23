#! /usr/bin/env python
#
#  ADMIT Flow Manager
#
#  Manages ADMIT tasks and flow
#
#

import sys, os, errno, fnmatch
from numpy.ma.core import ids
#import tasks

_debug = False
_debug = True

# ===================================================================================================

class FlowManager():
    """  Manages the flow of tasks, normally only used by ADMIT
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

    def __len__(self):
        """Return number of tasks under control of FlowManager"""
        return len(self.tasks)

    def __getitem__(self, index):
        """Return a task reference from the tasks dictionary"""
        return self.tasks[index]

    def make_depsmap(self):
        """ make dependency map from connection map """

        tmp_cmap = list(self.connmap)
        task_ids = self.tasks.keys()

        num = len(tmp_cmap)

        # we only loop through the connection map at most num times (worst case: only 
        # one task at each level) to prevent getting in an infinite loop if the 
        # connection map is not a good one
        while num > 0 and len(tmp_cmap) > 0 :
            num = num - 1
            roots = []
            roots = self.find_roots(tmp_cmap)
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
        if self.changed_conn or len(self.depsmap) == 0: 
            self.make_depsmap()

        for dl in self.depsmap:
            # the dl[] are tasks that are independent, and could be run in parallel
            for d in dl:
                if self.tasks[d].updated:
                    self.tasks[d].run()
                    self.tasks[d].updated = False

        self.depsmap = []

    def add(self, a, tuples = None):
        """Add an AT to the task list
           Usually all but the first task will have a List of Tuples (each tuple = (source AT, source BDP)).
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
                print "FM.add >>>>>>>",i,">>>>>>>>>"
                a.bdp_in.append( self.tasks[source_at_id][source_bdp_id] )

        return a.taskid

    def get_conn(self):
        return self.connmap;

    def show(self):
        print "=== FM: connection map", self.connmap
        print "=== FM: tasks ======="
        for key in self.tasks:
            print key, ":", self.tasks[key].name
        print "=== FM: dependency map", self.depsmap
        for cm in self.connmap:
            print "connmap", cm[0], cm[1], cm[2], cm[3]
            # print "       ", self.tasks[cm[0]].name, self.tasks[cm[0]][cm[1]].filename,self.tasks[cm[2]].name
            print "src task:", self.tasks[cm[0]].name
            print "bdp out:", self.tasks[cm[0]][cm[1]].filename
            print "des task:", self.tasks[cm[2]].name
            # print "bdp in:", self.tasks[cm[2]][cm[3]].filename  ## commented out because the following error:
                                                                  ## admit2.py", line 441, in __getitem__
                                                                  ## return self.bdp_out[index]
                                                                  ## IndexError: list index out of range

        for i in range(len(self.depsmap)):
            print "Level %d : %s" % (i,self.depsmap[i])
        for dl in self.depsmap:
            for d in dl:
                print "TASK %d: %s" % (d,self.tasks[d].name)

    def verify(self):
        """ verify the state of the FlowManager.
        Returns True or False.
        """
        tmp_cmap = list(self.connmap)
        num = len(tmp_cmap)

        # we only check the nodes num of times to prevent getting in an infinite loop
        while num > 0 and len(tmp_cmap) > 0 :
            roots = []
            roots = self.findroots(tmp_cmap)
            print num
            if len(roots) > 0 :
                for node in roots:
                    tmp_cmap.remove(node)  ## remove the root nodes

            num = num -1

        if len(tmp_cmap) != 0:    ## no root found - this connection map is not valid
            return False
        else:
            return True
            
    def find_roots(self, cmap=None):
        """ find roots of a connection map """
        if cmap == None:
            tmp_map = self.connmap
        else:
            tmp_map = cmap

        roots = []
        src_index = 0
        des_index = 2

        for cm in tmp_map:
            isroot = True

            # first check if this connection node points to itself
            if cm[src_index] == cm[des_index]:
                print "Self loop found:", cm
                return roots

            for cm2 in tmp_map:
                if cm[src_index] == cm2[des_index]:
                    # if the source task is found within destination tasks, then it is not a root
                    isroot = False
                    pass

            if isroot:
                print "root connection node:", cm
                roots.append(cm)

        return roots

    def get_downstream(self, at_taskid):
        """ get the downstream ATs of this task """

        i = at_taskid
        tmp = [i]
        downstream_tasks = []
        tmp_cmap = list(self.connmap)
        src_index = 0
        des_index = 2
        while len(tmp) > 0 :
            #print tmp
            #id = tmp.pop()

            id = tmp[0]
            tmp.remove(id)
            downstream_tasks.append(id)

            for cm in tmp_cmap:
                if cm[src_index] == id:
                    #print "FOUND", cm
                    des = cm[des_index]

                    # now check if this task is already in tmp
                    toAppend = True
                    for t in tmp:
                        if des == t:
                            toAppend = False
                            pass

                    if toAppend:
                        tmp.append(des)

        return downstream_tasks

    def insert(self, at, bout, cm_tuple):
        """ inserting an AT into a connection map tuple: cm
            bout is the output of the AT to be inserted
            example: cm_tuple = (ai,bi, aj,bj) = (cm[0],cm[1], cm[2],cm[3])
                     insert ax with bx output

            result: (ai,bi, ax,bi) (ax,bx, aj,bx)
        """

        # remember the position of cm_tuple
        pos = self.connmap.index(cm_tuple)

        # find the tuple in connection map
        count = self.connmap.count(cm_tuple)
        if count > 0 :
            self.connmap.remove(cm_tuple)
        else:
            print "Not Found:", cm_tuple
            return False

        self.tasks[at.taskid] = at
        ai = self.tasks[cm_tuple[0]]
        at.bdp_in.append( ai[cm_tuple[1]] )

        aj = self.tasks[cm_tuple[2]]
        aj.bdp_in.append(at[bout])
        new1 = (cm_tuple[0], cm_tuple[1], at.taskid, cm_tuple[1])
        new2 = (at.taskid, bout, cm_tuple[2], bout)

        self.connmap.insert(pos, new1)
        self.connmap.insert(pos+1, new2)

        return True

    def update(self, at):
        """ set the updated flag of an AT and its downstream ATs """

        taskid = at.taskid
        all_at = self.get_downstream(taskid)
        for a in all_at:
            a.updated = True

    def test_flow4(self):
        self.connmap = [(0, 0, 1, 0), (0, 0, 2, 0), (1, 0, 3, 0), (2, 0, 3, 1)]
        self.connmap = [("a0", 0, "a1", 0), ("a0", 0, "a2", 0), ("a1", 0, "a3", 0),("a2", 0, "a3", 1)]
        #self.connmap = [("a0", 0, "a1", 0), ("a0", 0, "a2", 0), ("a1", 0, "a3", 0),("a2", 0, "a3", 1),("a3", 0, "a1", 1)]
        print self.connmap;


# fm = FlowManager()
# fm.test_flow4()
# tasks = fm.get_downstream('a1')
# print tasks
