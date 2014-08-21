#! /usr/bin/env python
#
#
#
import sys, os
import copy
import cPickle as pickle
import atable

_debug = False
_debug = True

nprojects = 100
nlines    = 100

class ADMIT(object):
    def __init__(self, name='none'):
        self.name    = name
        self.bdps    = []
    def __len__(self):
        return len(self.bdps)
    def __eq__(self, other):
        return isinstance(other, ADMIT) and vars(self) == vars(other)
    def add(self, b):
        """Add a BDP to the stack of BDP's this ADMIT pipeline contains"""
        b1 = copy.deepcopy(b)
        self.bdps.append(b1)
    def set(self,a=None, b=1, c=[]):
        """set a global ADMIT parameter
           The idea is that these are obtained through introspection
        """
        print "ADMIT: set" 
        if a != None:  print 'a: ',a
    def get(self,key):
        """get a global ADMIT parameter"""
        print "ADMIT: get=%s" % key
    def print_methods(self):
        """ print all the methods of this object and their doc string"""
        print '\n* Methods *'
        for names in dir(self):
            attr = getattr(self,names)
            if callable(attr):
                print names,':',attr.__doc__
    def print_attributes(self):
        """ print all the attributes of this object and their value """
        print '* Attributes *'
        for names in dir(self):
            attr = getattr(self,names)
            if not callable(attr):
                print names,':',attr
    def print_all(self):
        """ calls all the methods of this object """
        for names in dir(self):
            attr = getattr(self,names)
            if callable(attr) and names != 'print_all' and names != '__init__':
                attr() # calling the method
    def pdump(self,name=None):
        if not name:
            pname = self.name + '.p'
        else:
            pname = name
        print "ADMIT: pickle saving %s" % pname
        pickle.dump(self,open(pname,"wb"))


class BDP(object):
    def __init__(self, name='none', filename='foobar'):
        self.name     = name
        self.filename = filename
        self.updated  = False
        self.deps     = []
        self.derv     = []
        self.task     = []
        if _debug: print "BDP(%s) " % name
    def show(self):
        return self.name
    def update(self,new_state):
        if _debug: print "UPDATE: %s" % self.name
        self.updated = new_state
        for d in self.derv:
            d.update(new_state)
    def depends_on(self,other):
        if other == None: return
        if _debug: print 'BDP %s depends on %s' % (self.name,other.show())
        self.deps.append(other)
        other.derv.append(self)
    def report(self):
        print "===report==="
        print "BDP::%s" % self.name
        for d in self.deps:
            print "BDP::deps %s" % d.show()
        for d in self.derv:
            print "BDP::derv %s" % d.show()
        for t in self.task:
            print "BDP::task %s" % t.show()
    def set(self,keyval):
        if _debug: print "BDP::set %s" % keyval
    def run(self):
        if self.updated: 
            if _debug: print "BDP::%s (%s) was up to date" % (self.name,self.filename)
            return False
        if _debug: print "BDP::%s (%s) running" % (self.name,self.filename)
        if len(self.task) == 0:
            if _debug: print " Warning: no task set ???"
            # raise ?
        else:
            for t in self.task:
                t.run()
        self.updated = True
        return True

def DependsOn(a,b):
    """ b depends on a """
    b.depends_on(a)

class AT(object):
    name    = 'generic'
    version = '1.0'
    keys    = ['alpha', 'beta', 'gamma']
    def __init__(self,name='none',bdp_in=[],bdp_out=[]):
        if _debug: print "AT.init(%s)" % name
        self.name    = name
        self.dop     = True
        self.bdp_in  = bdp_in
        self.bdp_out = bdp_out
        for b2 in bdp_out:
            b2.task.append(self)
            for b1 in bdp_in:
                if b1 != b2:
                    b2.depends_on(b1)
    def show(self):
        return self.name
    def run(self):
        if _debug: print "AT.run(%s)" % self.name
        do_nothing = True
        for b2 in self.bdp_out:
            if not b2.updated: do_nothing = False
        if do_nothing:
            if _debug: print "   no work needed here"
            return False
        for b2 in self.bdp_out:
            b2.updated = True
        return True
    def set(self,keyval):
        for b2 in self.bdp_out:
            if b2.updated:
                b2.update(False)
    def rerun(self):
        if _debug: print "AT.rerun(%s)" % self.name
    def report(self):
        print "AT: ",self.name
        if len(self.bdp_in) > 0:
            print "  BDP_IN:"
            for b in self.bdp_in:  print "    ",b.show()
        if len(self.bdp_out) > 0:
            print "  BDP_OUT:"
            for b in self.bdp_out:  print "    ",b.show()


class AT_ingest(AT):
    name = 'INGEST'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_ingest.init"
    def run(self):
        if _debug: print "AT_ingest.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        if len(self.bdp_in) > 0:
            print "AT_ingest: no BDP_in expected"
        if len(self.bdp_out) != 1:
            print "AT_ingest: only one BPD_out expected"
        if self.dop:
            pname = self.bdp_out[0].filename + ".pb"
            print "AT_ingest: writing ",pname
            pickle.dump(self.bdp_out[0],open(pname,"wb")) 

class AT_cube(AT):
    name = 'CUBE'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_cube.init"
    def run(self):
        if _debug: print "AT_cube.run"
        if not AT.run(self):
            return False
        # specialized work can commence here



class AT_cubestats(AT):
    name = 'CUBESTATS'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_cubestats.init"
    def run(self):
        if _debug: print "AT_cubestats.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        os.system('cubestats in=%s')
        a0 = atable.ATable()
        a1 = a0.pload('cubestats.bin')
        print a1.names
        self.bdp_out[0].table = a1
        if self.dop:
            pname = self.bdp_out[0].filename + ".pb"
            print "AT_cubestats: writing ",pname
            pickle.dump(self.bdp_out[0],open(pname,"wb")) 



class AT_combine(AT):
    name = 'COMBINE'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_combine.init"
    def run(self):
        if _debug: print "AT_combine.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        print "  work: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        print "  in:  ",self.bdp_in[0].show(),self.bdp_in[1].show()
        print "  out: ",self.bdp_out[0].show()



class AT_flow(AT):
    name = 'FLOW'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        if _debug: print "AT_flow.init"
        AT.__init__(self,self.name,bdp_in,bdp_out)
        set_keys=self.set.im_func.func_code.co_varnames
        set_vals=self.set.im_func.func_defaults
        print 'keys:',set_keys
        print 'vals:',set_vals
    # note the deliberate bug to not implement the .run() here
    def run(self):
        if _debug: print "AT_flow.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        print "  work_flow: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        #
        if self.dop:
            pname = self.bdp_out[0].filename + ".pb"
            print "AT_ingest: writing ",pname
            pickle.dump(self.bdp_out[0],open(pname,"wb")) 
    def set(self,a=None, b=1, c=[], d='d'):
        """AT.set() is the way parameters are passed"""
        print "AT.set"
    def get(self,key):
        """AT.get() retrieved current values"""
        print "AT.get"

class AT_flow2(AT):
    name = 'FLOW2'
    version = '2.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        if _debug: print "AT_flow2.init"
        AT.__init__(self,self.name,bdp_in,bdp_out)
    # note the deliberate bug to not implement the .run() here
    def run(self):
        if _debug: print "AT_flow2.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        print "  work_flow2: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))


# running a series of BDP's is not right if BDP's can have different state
# but this is one way to run the pipeline.
# it is also assumed the BDPs are sorted in the right order, so no BDP
# depends on a BDP later in the list
def pipeline(bdps):
    if _debug: print "===============   Running BDP based pipeline ============="
    for b in bdps:
        b.run()

def try1a(do_show=True, do_dep=True):
    _debug = True
    print "TRY1a"
    #  start a new ADMIT
    a = ADMIT("TRY1a")

    #  b0 is the BDP that simply contains the FITS file we're working on
    b0 = BDP('fits','im/fits')               ; a.add(b0)
    a1 = AT_ingest([],[b0])      
    a1.run()

    b1 = BDP('cube','im/cim')                ; a.add(b1)
    a2 = AT_flow([b0],[b1])
    a2.run()

    b2 = BDP('cubestats','im/cubestats')
    a3 = AT_cubestats([b1],[b2])             ; a.add(b2)
    a3.run()

    a.pdump()

if __name__ == "__main__":
    a = try1a()
