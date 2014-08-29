#! /usr/bin/env python
#
#
#  simple container to put all of the ADMIT, BDP and AT in one file for testing
#
#  no 'import casa' or so allowed here. All package specific work needs to be delegated
#
import sys, os
import copy
import cPickle as pickle
import atable
import matplotlib.pyplot as plt
import numpy as np

_debug = False
_debug = True

nprojects = 100
nlines    = 100

# ==============================================================================

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
        # note there needs to be a cleanup/delete/pop option here
        # __main__ : deepcopy ga ve 19780 bytes,  re-assign + deepcopy was 22973 bytes, why ?
        if False:
            b1 = copy.deepcopy(b)
            self.bdps.append(b1)
        else:
            self.bdps.append(b)
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
        self.bdp_out[0].data['table'] = a1
        self.table = a1
        freq   = a1.get('frequency')/1e9        # in GHz now
        noise  = a1.get('medabsdevmed')*1000    # in mJy/beam now
        signal = a1.get('max')*1000             # in mJy/beam now
        print 'freq type ',freq.dtype
        print "Freq range : %g %g GHz" % (freq.min(), freq.max())
        print "Noise range : %g %g mJy/beam" % (noise.min(), noise.max())
        print "Peak Signal range : %g %g mJy/beam" % (signal.min(), signal.max())
        filename = self.bdp_out[0].filename 
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            a1.plotter(freq,[np.log(signal),np.log(noise)],'CubeStats',filename+'.png')
            
class AT_cubespectrum(AT):
    name = 'CUBESPECTRUM'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_cubespectrum.init"
    def run(self):
        if _debug: print "AT_cubespectrum.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        os.system('cubespectrum in=%s')
        a0 = atable.ATable()
        a1 = a0.pload('cubespectrum.bin')
        print a1.names
        self.bdp_out[0].data['table'] = a1
        freq   = a1.get('frequency')/1e9        # in GHz now
        data   = a1.get('data')*1000            # in mJy/beam now
        print 'freq type ',freq.dtype
        print "Freq range : %g %g GHz" % (freq.min(), freq.max())
        print "Data range : %g %g mJy/beam" % (data.min(), data.max())
        filename = self.bdp_out[0].filename 
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            a1.plotter(freq,[data],'CubeSpectrum',filename+'.png')


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
    # note the deliberate bug to not implement the .run() here
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
