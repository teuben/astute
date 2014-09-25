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
 
# class AT_simple(AT):
#     """
#     A simple AT_xxx class with only the basic things present
#     """
#     name    = 'SIMPLE'
#     version = '1.0'
#     keys    = []
#     def __init__(self):
#         AT.__init__(self,self.name)
#     def run(self):
#         if not AT.run(self): return False
#         # do your work:
#         #     self.bdp_in[] and self.bdp_out[] contain BDP's 
#         #     ... contain parameters
# 
# class AT_file(AT):
#     """ Create a simple container for a file, with no further description.
# 
#         bdp_in[]:    none
#         bdp_out[0]:  filename
#     """
#     name    = 'FILE'
#     version = '1.0'
#     keys    = ['file','touch']
#     def __init__(self,name=None):
#         if name != None: self.name = name
#         AT.__init__(self,self.name)
#         if _debug: print "AT_file.init"
#         self.bdp_out = [BDP_file(self.name)]
#     def check(self):
#         print "CHECK AT_file"
#     def run(self):
#         if _debug: print "AT_file.run"
#         if not AT.run(self):
#             return False
#         if self.getb('touch',0):
#             fn = self.bdp_out[0].filename
#             print "TOUCHING",fn
#             os.system('touch %s' % fn)
#         #
# 
#         if self.do_pickle:
#             self.pdump()
# 
# class AT_cube(AT):
#     name    = 'CUBE'
#     version = '1.0'
#     keys    = []
#     def __init__(self,bdp_in=[],bdp_out=[]):
#         AT.__init__(self,self.name,bdp_in,bdp_out)
#         if _debug: print "AT_cube.init"
#     def run(self):
#         if _debug: print "AT_cube.run"
#         if not AT.run(self):
#             return False
#         # specialized work can commence here
# 
# 
# # the classes below are for playing with pipelines, they do no real work.
# #
# # flow:   1 -> 1
# # flow12: 1 -> 2
# # flow21: 2 -> 1
# # flow1N: 1 -> N 
# # flowN1: N -> 1
# #
# 
# class AT_flow(AT):
#     """ change one BDP into another one"""
#     name = 'FLOW'
#     version = '1.0'
#     keys = ['debug','touch']
#     def __init__(self,name=None):
#         if name != None: self.name = name
#         if _debug: print "AT_flow.init"
#         AT.__init__(self,self.name)
# 
#         b = BDP_file(self.name)
#         self.bdp_out = [b]
#     def run(self):
#         if _debug: print "AT_flow.run(%s)" % self.name
#         if not AT.run(self):
#             return False
#         print "  work_flow: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
#         if self.getb('touch',0):
#             fn = self.bdp_out[0].filename
#             print "TOUCHING",fn
#             os.system('touch %s' % fn)
#         #
#         if self.do_pickle:
#             self.pdump()
#   
# 
# class AT_flow12(AT):
#     """ split one BDP into two """
#     name = 'FLOW12'
#     version = '1.0'
#     keys = ['debug','touch']
#     def __init__(self,name=None):
#         if name != None: self.name = name
#         if _debug: print "AT_flow12.init"
#         AT.__init__(self,self.name)
#         b1 = BDP_file(self.name + '.1')
#         b2 = BDP_file(self.name + '.2')
#         self.bdp_out = [b1,b2]
#     def run(self):
#         if _debug: print "AT_flow12.run(%s)" % self.name
#         if not AT.run(self):
#             return False
#         # specialized work can commence here
#         print "  work_flow12: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
#         if self.getb('touch',0):
#             for i in [0,1]:
#                 fn = self.bdp_out[i].filename
#                 print "TOUCHING",fn
#                 os.system('touch %s' % fn)
#         if self.do_pickle:
#             self.pdump()
# 
# class AT_flow21(AT):
#     """ combine two BDPs into one"""
#     name = 'FLOW21'
#     version = '1.0'
#     keys = ['debug','touch']
#     def __init__(self,name=None):
#         if name != None: self.name = name
#         AT.__init__(self,self.name)
#         if _debug: print "AT_flow21.init"
#         b = BDP_file(self.name)
#         self.bdp_out = [b]
#     def run(self):
#         if _debug: print "AT_flow21.run(%s)" % self.name
#         if not AT.run(self):
#             return False
#         # specialized work can commence here
#         print "  work: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
#         print "  in:  ",self.bdp_in[0].show(),self.bdp_in[1].show()
#         print "  out: ",self.bdp_out[0].show()
#         if self.getb('touch',0):
#             fn = self.bdp_out[0].filename
#             print "TOUCHING",fn
#             os.system('touch %s' % fn)
#         if self.do_pickle:
#             self.pdump()
# 
# class AT_flow22(AT):
#     """ arrange two BDPs into two others"""
#     name = 'FLOW22'
#     version = '1.0'
#     keys = ['debug']
#     def __init__(self,bdp_in=[],bdp_out=[],name=None):
#         if name != None: self.name = name
#         AT.__init__(self,self.name,bdp_in,bdp_out)
#         if _debug: print "AT_flow22.init"
#     def run(self):
#         if _debug: print "AT_flow22.run(%s)" % self.name
#         if not AT.run(self):
#             return False
#         # specialized work can commence here
#         print "  work: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
#         print "  in:  ",self.bdp_in[0].show(),self.bdp_in[1].show()
#         print "  out: ",self.bdp_out[0].show()
#         if self.do_pickle:
#             self.pdump()
# 
# class AT_flow1N(AT):
#     """Split one BDP into N BDPs.  The value of N is perhaps not known before entry, but this
#     differs how the AT should handle this:
#     1) caller knows N and allocates the array bdp_out[] and the AT fills them
#     2) caller does not know N (e.g. it depends on the bdp_in[] and keys[]), and 
#        can give either an empty bdp[] or a single [b] , the AT will then allocate
#        and add to this list. This however means that the AT needs to make decisions
#        on naming convention, in either case.
#     """
#     name = 'FLOW1N'
#     version = '1.0'
#     keys = ['n','debug','touch']
#     def __init__(self,name=None):
#         if name != None: self.name = name
#         if _debug: print "AT_flow1N.init"
#         AT.__init__(self,self.name)
#         # note we cannot allocate BDP's because we don't know N yet
#         # thus the run() task will need to broadcast the information
#         # for admit to pick this up
#         # but....
#         # bdp_in set in a.add()
#         # bdp_out set in constructor (normally)
#     def check(self):
#         print "CHECK AT_flow1N "
#         n = self.geti('n',0)
#     def run(self):
#         if _debug: print "AT_flow1N.run(%s)" % self.name
#         if not AT.run(self):
#             return False
#         # specialized work can commence here
#         n = self.geti('n',0)
#         b=[]
#         for i in range(n):
#             b.append(BDP_file(self.name+'.%d'%(i+1)))
#         self.bdp_out = b
# 
#         print "  work_flow1N: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
#         if self.getb('touch',0):
#             for i in range(n):
#                 fn = self.bdp_out[i].filename
#                 print "TOUCHING",fn
#                 os.system('touch %s' % fn)
# 
#         if self.do_pickle:
#             self.pdump()
# 
# class AT_flowN1(AT):
#     """Take BDPs, merge them into one"""
#     name = 'FLOWN1'
#     version = '1.0'
#     keys = ['debug']
#     def __init__(self,bdp_in=[],bdp_out=[],name=None):
#         if name != None: self.name = name
#         if _debug: print "AT_flowN1.init"
#         AT.__init__(self,self.name,bdp_in,bdp_out)
#     def run(self):
#         if _debug: print "AT_flowN1.run(%s)" % self.name
#         if not AT.run(self):
#             return False
#         # specialized work can commence here
#         print "  work_flowN1: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
#         if self.do_pickle:
#             self.pdump()
# 
# 
# # running a series of BDP's is not right if BDP's can have different state
# # but this is one way to run the pipeline.
# # it is also assumed the BDPs are sorted in the right order, so no BDP
# # depends on a BDP later in the list
# def pipeline(bdps):
#     if _debug: print "===============   Running BDP based pipeline ============="
#     for b in bdps:
#         b.run()
# 
# if __name__ == "__main__":
# 
#     # pickle files store the module name, so keep that here, 
#     # since that is how we run it externally
#     import admit1 as admit
# 
#     #  silly stuff to limit the flow of the pipeline (Q=0 only produces b0, Q=1 the b1, etc.)
#     Q = 0
#     if len(sys.argv)>1:
#         Q = int(sys.argv[1])
#     #
#     print "TESTING admit1.py:"
#     #
#     a = admit.ADMIT()
#     if Q>=0:
#         b0 = admit.BDP_file("b0")
#         a0 = admit.AT_file([],[b0])
#         a0.run()
#         a.add(b0)
#         if Q>0:
#             b1 = admit.BDP_buckett("b1")
#             a1 = admit.AT_flow([b0],[b1])
#             a1.run()
#             a.add(b1)
#             if Q>1:
#                 b21 = admit.BDP_buckett("b21")
#                 b22 = admit.BDP_buckett("b22")
#                 a2 = admit.AT_flow12([b1],[b21,b22])
#                 a2.run()
#                 a.add(b21)
#                 a.add(b22)
#                 if Q>2:
#                     b3 = admit.BDP_buckett("b3")
#                     a3 = admit.AT_flow21([b21,b22],[b3])
#                     a3.run()
#                     a.add(b3)
#                     if Q>3:
#                         n = 10
#                         b4 = range(n)
#                         for i in range(n):
#                             id = "b4_%d" % i
#                             b4[i] = admit.BDP_buckett(id)
#                         a4 = admit.AT_flowN([b3],b4)
#                         a4.run()
#                         for i in range(n):
#                             a.add(b4[i])
#     # a0.pdump('test00.p')
#     a.pdump('admit1.p')
#     b0.pdump('b00.p')
#     print "Q=%d" % Q
