#! /usr/bin/env python
#
#
#  simple container to put all of the ADMIT, BDP and AT in one file for testing
#
#  no 'import casa' or so allowed here. All package specific work needs to be delegated
#
import sys, os, errno, fnmatch
import copy
import cPickle as pickle
import atable
import matplotlib.pyplot as plt
import numpy as np
import parfile

_debug = False
_debug = True

nprojects = 100
nlines    = 100

# ==============================================================================

class ADMIT(object):
    def __init__(self, name='none'):
        self.parfile = "tas.def"       #  relic of ASTUTE, keep it for now
        self.name    = name
        self.debug   = False
        self.bdps    = []
    def __len__(self):
        return len(self.bdps)
    def __eq__(self, other):
        return isinstance(other, ADMIT) and vars(self) == vars(other)
    def add(self, b):
        """Add a BDP to the stack of BDP's this ADMIT pipeline contains"""
        # note there needs to be a cleanup/delete/pop option here
        # __main__ : deepcopy ga ve 19780 bytes,  re-assign + deepcopy was 22973 bytes, why ?
        if False:
            b1 = copy.deepcopy(b)
            self.bdps.append(b1)
        else:
            self.bdps.append(b)
    def run(self):
        """from all the BDP's are known, and their relation ship,
        this will run the whole pipeline, but not the orphans
        """
        print "no run in admit yet"
    def set(self,a=None, b=1, c=[]):
        """set a global ADMIT parameter
           The idea is that these are obtained through introspection
        """
        print "ADMIT: set" 
        if a != None:  print 'a: ',a
    def check(self):
        """ check all the BDP's in this admit, and see if they have name collisions
        of their BDPs, and identify orphaned branches of the tree
        """
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
        btmp = self.bdps
        self.bdps = []
        for b in btmp:
            b1 = copy.deepcopy(b)
            self.bdps.append(b1)
        pickle.dump(self,open(pname,"wb"))
        del btmp
    def pload(self,pname):
        print "ADMIT: pickle loading %s" % pname
        return pickle.load(open(pname,"rb"))
    def discover(self,mode=None,rootdir='.'):
        print "query_dir() and find_files() are the worker functions"
        print "discover not implemented yet"
        pp = []
        return pp
    def query_dir(self,here=None):
        """
        from here, drill down and find directories in which ADMIT exists
        """
        dlist = []
        if here == None:
            path = "."
        else:
            path = here
        n = 0
        for path, dirs, files in os.walk(path):
            # better not to loop, but os.path() for existence
            n = n + 1
            for f in files:
                if f == self.parfile: dlist.append(path)
        if self.debug: print "Queried ",n," directories, found ",len(dlist), " with a parfile"
        return dlist
    def find_files(self, pattern="*.fits"):
        """
        Find files containing a wildcard pattern
        """
        flist = []
        for file in os.listdir('.'):
            if fnmatch.fnmatch(file,pattern):
                flist.append(file)
        return flist
    def setdir(self,dirname, create=True):
        """
        change directory to dirname to work in. Assumed to contain parameter file
        if the directory doesn't exist yet, create it
        """
        def mkdir_p(path):
            #if not os.path.isdir(dirname):
            #    os.makedirs(dirname)
            #
            try:
                os.makedirs(path)
            except OSError as exc: # Python >2.5
                if exc.errno == errno.EEXIST and os.path.isdir(path):
                    pass
                else: raise
        self.p = dirname
        self.pwd = os.getcwd()
        if create: mkdir_p(dirname)
        os.chdir(dirname)
        if self.debug: print "ADMIT::setdir %s" % dirname
    def tesdir(self):
        """
        revert back from previous setdir (sorry, not recursive yet)
        """
        os.chdir(self.pwd)
    def walkdir(self,dlist):
        print "Walkdir ",dlist
        for d in dlist:
            self.setdir(d)
            print "d: ",d
            par = pp.ParFile()
            print par.get('fits')
            print par.keys()
            self.tesdir()




# ==============================================================================

class BDP(object):
    """ Base class for BDP
        should have some static members
    """
    #
    def __init__(self, name='none',filename=None, filetype=None):
        self.name     = name
        self.id       = 0
        self.filename = filename
        self.filetype = filetype
        self.data     = {}
        #
        self.updated  = False     # ???   this triggers a new run
        self.output   = True      # True: triggers a new save(pdump/xwrite)
        self.deps     = []
        self.derv     = []
        self.task     = []
        if _debug: print "BDP(%s,%s,%s) " % (name,filename,filetype)
    def parse(self,doParse = True):
        """ Doug's XML parser, automatically invoked if
            you do b = BDP_foobar("xmlfile")
        """
    def write(self,xmlFile = None):
        """ Doug's XML writer
        """
    def show(self):
        return self.filename
    def info(self):
        print 'BDP %s(%s)' % (self.name,self.filename)
        if len(self.deps)==0:
            print 'deps: -'
        else:
            print 'deps: '
            for bi in self.deps:
                print '    : %s(%s)' % (bi.name, bi.filename)
        if len(self.derv)==0:
            print 'derv: -'
        else:
            print 'derv:'
            for bi in self.derv:
                print '    : %s(%s)' % (bi.name, bi.filename)
        t = self.task[0]
        print 'TASK ',t.name
        print '     ',t.keys
        print '     ',t.keyvals

    def update(self,new_state):
        if _debug: print "UPDATE: %s" % self.name
        self.updated = new_state
        for d in self.derv:
            d.update(new_state)
    def depends_on(self,other):
        if other == None: return
        if _debug: print 'BDP %s depends on %s' % (self.filename,other.show())
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
    def pdump(self,filename):
        """ save, if needed """
        if self.output:
            if _debug: print "BDP.pdump(%s)" % filename
            pickle.dump(self,open(filename,"wb"))
            self.output = False
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

class BDP_buckett(BDP):
    """
    This BDP is a random collection of things you find useful. Less rigurous testing
    and verfication on valid data is done here, and gets you going quickly for
    using is.
    Use the dictionary member data{} to place anything you like
    e.g.   b.data['table1'] = my_atable
    This pickles ok, but must be a nightmare for XML. 
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"BUCKETT",filename,filetype)


class BDP_file(BDP):
    """
    Contains a reference to a dataset (fits file, casa image, ...)
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"FILE", filename, filetype)

class BDP_table(BDP):
    """
    Contains a reference to a table (shouldn't BDP_file suffice?)
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"TABLE", filename, filetype)
        self.table = []

class BDP_cubestats(BDP):
    """
    Contains a reference to a cubestats table
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"CUBESTATS", filename, filetype)
        self.table = []
        self.mean  = None
        self.sigma = None
        self.max   = None
        self.maxpos = []
    def set_table(self,t):
        self.table = t
    def get_table(self):
        return self.table

class BDP_cubespectrum(BDP):
    """
    Contains a reference to a cubespectrum table
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"CUBESPECTRUM", filename, filetype)
        self.table = []
    def set_table(self,t):
        self.table = t
    def get_table(self):
        return self.table


# ==============================================================================

class AT(object):
    # not really static accross instantiations
    env     = 'casa'
    name    = 'generic'
    version = '1.0'
    keys    = []
    def __init__(self,name='none',bdp_in=[],bdp_out=[]):
        if _debug: print "AT(%s,[%d],[%d])" % (name,len(bdp_in),len(bdp_out))
        self.name      = name
        self.do_pickle = True
        self.do_plot   = True
        self.bdp_in    = bdp_in
        self.bdp_out   = bdp_out
        self.keyvals   = {}
        for b2 in bdp_out:
            b2.task.append(self)
            for b1 in bdp_in:
                if b1 != b2:
                    b2.depends_on(b1)
                    b1.output = True
                else:
                    # formally, b1 should never be b2
                    print "bad bad bad, b1==b2"
                    
    def show(self):
        return self.name
    def run(self):
        """ run the task, but the only thing this returns is a True or False
        to designate if the BDP's were up to date.  Returns True if the real
        AT_xxx needs to run.
        """
        # if _debug: print "AT.run(%s)" % self.name
        do_nothing = True
        for b2 in self.bdp_out:
            if not b2.updated: do_nothing = False
        if do_nothing:
            if _debug: print "   no work needed here"
            return False
        for b2 in self.bdp_out:
            b2.updated = True
            b2.output  = True
        return True
    def setenv(self,newval):
        # playing with env
        self.env = newval
    def getenv(self):
        # why is env not available
        return self.env
    def set(self,keyvals):
        kv = keyvals.split('=')
        self.setkv({ kv[0] : kv[1] })
    def setkv(self,keyvals):
        """set a task parameter"""
        # store them, but should also check if valid
        print "set keys: ",self.keys
        for k in keyvals.keys():
            self.keyvals[k] = keyvals[k]
        # mark all bdp's that they have changed information
        for b2 in self.bdp_out:
            if b2.updated:
                b2.update(False)
    def get(self, key):
        return self.keyvals[key]
    def has(self, key):
        return self.keyvals.has_key(key)
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
    def pdump(self, ext='p'):
        """  pickle dumps all the output BDP's
             @todo   parents need to be signalled if they have new children
                     so they need to save their state if BDP's are saved
                     after every .run
                     
        """
        for b in self.bdp_out:
            pname = b.filename + "." + ext
            b.pdump(pname)
        # also check the inputs, since they may <have new dependencies
        for b in self.bdp_in:
            pname = b.filename + "." + ext
            b.pdump(pname)

    def pload(self, ext='p', filename=None):
        """ is this even sane? """
        if filename:
            self.bdp_in[0] = pickle.load(open(filename,"rb"))
            return self.bdp_in[0]
        else:
            for b in self.bdp_in:
                pname = b.filename + '.' + ext
                print "reading ",pname
                b = pickle.load(open(pname,"rb"))


class AT_simple(AT):
    """
    A simple AT_xxx class with only the basic things present
    """
    name    = 'SIMPLE'
    version = '1.0'
    keys    = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not AT.run(self): return False
        # do your work:
        #     self.bdp_in[] and self.bdp_out[] contain BDP's 
        #     ... contain parameters

class AT_file(AT):
    """ Create a simple container for a file
        bdp_in:   none
        bdp_out:  one file
    """
    name    = 'FILE'
    version = '1.0'
    keys    = ['type']
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_file.init"
    def run(self):
        if _debug: print "AT_file.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        if len(self.bdp_in) > 0:
            print "AT_file: no BDP_in expected, ignored"
        if len(self.bdp_out) != 1:
            print "AT_file: only one BPD_out expected, only first one saved"
        if self.do_pickle:
            self.pdump()

class AT_ingest(AT):
    name    = 'INGEST'
    version = '1.0'
    keys    = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_ingest.init"
    def run(self):
        if _debug: print "AT_ingest.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        if len(self.bdp_in) != 1:
            print "AT_ingest: only one BDP_in expected"
        if len(self.bdp_out) != 1:
            print "AT_ingest: only one BPD_out expected"
        if self.do_pickle:
            self.pdump()


class AT_cube(AT):
    name    = 'CUBE'
    version = '1.0'
    keys    = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_cube.init"
    def run(self):
        if _debug: print "AT_cube.run"
        if not AT.run(self):
            return False
        # specialized work can commence here


# the classes below are for playing with pipelines, they do no real work.
#
# flow:   1 -> 1
# flow12: 1 -> 2
# flow21: 2 -> 1
# flowN:  1 -> N 
#

class AT_flow(AT):
    """ change one BDP into another one"""
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
    def run(self):
        if _debug: print "AT_flow.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        print "  work_flow: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        #
        if self.do_pickle:
            self.pdump()
    def set(self,a=None, b=1, c=[], d='d'):
        """AT.set() is the way parameters are passed"""
        print "AT.set"
    def get(self,key):
        """AT.get() retrieved current values"""
        print "AT.get"

class AT_flow12(AT):
    """ split one BDP into two """
    name = 'FLOW12'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        if _debug: print "AT_flow2.init"
        AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if _debug: print "AT_flow2.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        print "  work_flow2: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        if self.do_pickle:
            self.pdump()

class AT_flow21(AT):
    """ combine two BDPs into one"""
    name = 'FLOW21'
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
        if self.do_pickle:
            self.pdump()

class AT_flow22(AT):
    """ arrange two BDPs into two others"""
    name = 'FLOW22'
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
        if self.do_pickle:
            self.pdump()

class AT_flowN(AT):
    """Split one BDP into N BDPs"""
    name = 'FLOWN'
    version = '1.0'
    keys = ['n']
    def __init__(self,bdp_in=[],bdp_out=[]):
        if _debug: print "AT_flowN.init"
        AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if _debug: print "AT_flowN.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        print "  work_flowN: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        if self.do_pickle:
            self.pdump()


# running a series of BDP's is not right if BDP's can have different state
# but this is one way to run the pipeline.
# it is also assumed the BDPs are sorted in the right order, so no BDP
# depends on a BDP later in the list
def pipeline(bdps):
    if _debug: print "===============   Running BDP based pipeline ============="
    for b in bdps:
        b.run()

if __name__ == "__main__":

    # pickle files store the module name, so keep that here, 
    # since that is how we run it externally
    import admit1 as admit

    #  silly stuff to limit the flow of the pipeline (Q=0 only produces b0, Q=1 the b1, etc.)
    Q = 0
    if len(sys.argv)>1:
        Q = int(sys.argv[1])
    #
    print "TESTING admit1.py:"
    #
    a = admit.ADMIT()
    if Q>=0:
        b0 = admit.BDP_file("b0")
        a0 = admit.AT_file([],[b0])
        a0.run()
        a.add(b0)
        if Q>0:
            b1 = admit.BDP_buckett("b1")
            a1 = admit.AT_flow([b0],[b1])
            a1.run()
            a.add(b1)
            if Q>1:
                b21 = admit.BDP_buckett("b21")
                b22 = admit.BDP_buckett("b22")
                a2 = admit.AT_flow12([b1],[b21,b22])
                a2.run()
                a.add(b21)
                a.add(b22)
                if Q>2:
                    b3 = admit.BDP_buckett("b3")
                    a3 = admit.AT_flow21([b21,b22],[b3])
                    a3.run()
                    a.add(b3)
                    if Q>3:
                        n = 10
                        b4 = range(n)
                        for i in range(n):
                            id = "b4_%d" % i
                            b4[i] = admit.BDP_buckett(id)
                        a4 = admit.AT_flowN([b3],b4)
                        a4.run()
                        for i in range(n):
                            a.add(b4[i])
    # a0.pdump('test00.p')
    a.pdump('admit1.p')
    b0.pdump('b00.p')
    print "Q=%d" % Q
