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
import aplot

import FlowManager as FM

_debug = False
#_debug = True

# ==============================================================================

def casa_argv(argv):
    """process the argv from a casarun script to a classic argv list
       such that the returned argv[0] is the casarun scriptname
    """
    lines = os.popen("casarun -c","r").readlines()
    n = int(lines[len(lines)-1].strip())
    return argv[n:]


# ==============================================================================

class ADMIT(object):
    projectid = 0
    def __init__(self, name='none', project=None):
        # the following items need to be persistent
        self.parfile   = "tas.def"       #  relic of ASTUTE, keep it for now
        self.name      = name
        self.project   = project
        self.fm        = FM.FlowManager() # Flow Manager
        self.keyval    = {}               # user dictionary
        self.pmode     = 0                # plot mode
        self.do_xml    = 0                # XML ?
        self.do_pickle = 0                # Pickle ?
        self.projects = [self]            # Virtual Projects?
        # maintain a projectid in case multiple admit's are present
        self.projectid = ADMIT.projectid
        ADMIT.projectid = ADMIT.projectid + 1
        self.debug     = False
    def __len__(self):
        # AT or P ?
        return len(self.projects)
    def __eq__(self, other):
        # not really used
        return isinstance(other, ADMIT) and vars(self) == vars(other)
    def __getitem__(self,index):
        """ 
        get access to an AT, and a BDP from there.
        """
        #print '__getitem__:',index
        #print 'str:',str(index),repr(index)
        # one index -> self.projects[index]
        # two index -> self.fm.tasks[index]
        # three index -> self.fm.tasks[index] -> bdp
        #return self.projects[index]
        return self.fm.tasks[index]
    def plotmode(self, plotmode, plottype='png'):
        """ plotmode determines if plots are saved, and in what format
            These are based on simple matplotlib diagrams
            Common output formats are png and pdf.
        """
        self.pmode = plotmode
        self.ptype = plottype
        # nasty cheat, need to formalize a safer method to talk to APlot
        aplot.APlot.pmode = plotmode
        print "plotmode: pmode=%d ptype=%s" % (self.pmode,self.ptype)
    def filemode(self, xml = 1, pickle =  0):
        """ filemode determines the output modes of files.
            It is possible to set all modes to 0, in which case there
            is no state output information saved, probably not a good
            idea. The default is just xml, nothing else.
        """
        self.do_xml     = xml
        self.do_pickle  = pickle
        print "filemode: xml=%d pickle=%d" % (self.do_xml,self.do_pickle)
    def addproject(self,p):
        """ Add another admit project to this project, expanding the
            virtual project
        """
        print 'addproject: ',len(self.projects)
        self.projects.append(p)
    def add(self, a, lot = None):
        """Add an AT to the stack of AT's this ADMIT contains
        Also adjust the mapping 
        Usually all but the first task will have a 'lot' (List of Tuples of source (task-id,bdp-id))
        @todo:  what if tuple is now (i,j,k) instead of (j,k) - if i>0 there needs to be an index
                into self.projects[]
        Returns the TaskID
        """
        # need to check if fm has been installed
        a.check()
        # task should inherit these from ADMIT
        a.pmode     = self.pmode
        a.do_pickle = self.do_pickle
        a.do_xml    = self.do_xml
        if len(a.bdp_in) != 0:
            print "WARNING WARNING: bdp_in not empty, somebody probably wrong here, did you use add() twice?"
        # now add the BDP_in's to the AT
        self.fm.add(a, lot)
        return a.taskid
    def run(self):
        """This will run those pieces of the pipeline flow
        that were deemed out of date. Perhaps it should also
        call runcheck() first?
        """
        self.fm.run()
    def runcheck(self):
        """ This will call the FlowManager and update all
        dependencies to ensure ALL dependent tasks are run
        """
        print "runcheck:"
    def info(self):
        print "ADMIT(%s): %s" % (self.name, self.project)
        for b in self.bdps:
            b.info()
    def show(self):
        print "=== ADMIT(%s): %s" % (self.name, self.project)
        self.fm.show()
        print "=== BDP's: " 
        # loop over all at's and show the BDP's
        for i in self.fm.tasks:
            t = self.fm.tasks[i]
            print "TASK: %s (%d)" % (t.name,len(t.bdp_out))
            for b in t.bdp_out:
                print "   bdp_out: %s" % b.filename
        print "BDP's:",self.query_bdp()
    def query_bdp(self,query=None):
        """ Query all BDP's in a PROJECT
        """
        lob = []
        if query == None:
            # loop over all at's and show the BDP's
            k = self.projectid 
            for pk in self.projects:
                k = pk.projectid
                for i in pk.fm.tasks:
                    t = pk.fm.tasks[i]
                    for j in range(len(t.bdp_out)):
                        lob.append( (k,i,j) )
        return lob
    def set(self,**kwargs):
        """set one or more global ADMIT parameters
        @todo  *args vs. **kwargs
        cf. the set() function in the AT, which is still a single 'key=val'
        """
        print "ADMIT: set" 
        for key,val in kwargs.items():
            print "SET: ",key,val
    def check(self):
        """ check all the BDP's in this admit, and see if they have name collisions
        of their BDPs, and identify orphaned branches of the tree
        A topological sort is needed as well, if they are not in the correct
        execution order.  See also the unix tsort(1) program 
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
        """ dump an admit object into pickle format
        """
        if not name:
            pname = self.name + '.p'
        else:
            pname = name
        print "ADMIT: pickle saving %s" % pname
        pickle.dump(self,open(pname,"wb"))
    def pload(self,pname):
        """ load an admit object into pickle format
            since admit stores many objects in deeply nested structures
            (the AT's and BDP's) they are duplicated. After a pickle.load()
            these should be re-pointed?
        """
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
        See pushd()/popd() for a better version - deprecate this.
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
        See pushd()/popd() for a better version
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



#
# ==============================================================================

class BDP(object):
    """ 
    Base class for all BDPs
    """
    bdpid = 0
    #
    def __init__(self, name='none',filename=None, filetype=None, project=None):
        self.taskid   = -1        # will be >=0 once set by the AT
        self.name     = name
        self.filename = filename
        self.filetype = filetype
        self.project  = project
        self.task     = []        # task with which BDP was created (should be 1)
        # below these are for runtime, not needed for persistence
        self.updated  = None      # deprecated
        self.output   = True      # True: triggers a new save(pdump/xwrite)
        self.pmode    = 0         # plotting mode (can be changed by admit)
        self.bdpid    = BDP.bdpid
        BDP.bdpid     = BDP.bdpid + 1
        if _debug: print "BDP[%d](%s,%s,%s) " % (self.bdpid,name,filename,filetype)
    def admit(self,project):
        self.project = project
    def parse(self,doParse = True):
        """ Doug's XML parser, automatically invoked if
            you do b = BDP_foobar("xmlfile")
        """
    def write(self,xmlFile = None):
        """ Doug's XML writer
        """
    def show(self):
        return "BDP_%s(%s): " % (self.name,self.filename)
    def info(self):
        print '===> BDP %s(%s) <===' % (self.name,self.filename)
    def update(self,new_state):
        # deprecated
        if _debug: print "UPDATE: %s(%s)" % (self.name,self.filename)
        self.updated = new_state
    def depends_on(self,other):
        print "depends_on deprecated"
    def report(self):
        print "===report==="
        print "BDP::%s" % self.name
    def set(self,keyval):
        if _debug: print "BDP::set %s" % keyval

    def print_attributes(self):
        """ show the attributes of this object and their value """
        print '* Attributes *'
        for names in dir(self):
            attr = getattr(self,names)
            if not callable(attr):
                print names,':',attr
    def pdump(self,filename):
        """ save, if needed """
        if self.output:
            if _debug: print "BDP.pdump(%s)" % filename
            pickle.dump(self,open(filename,"wb"))
            self.output = False

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
        self.data     = {}

class BDP_summary(BDP):
    """
    This BDP is a convenient summary of a project
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"SUMMARY",filename,filetype)
        self.data     = {}



class BDP_file(BDP):
    """
    Contains a reference to a dataset with no further distinctive info,
    just the filename. This makes it look like the baseclass BDP
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"FILE", filename, filetype)

class BDP_image(BDP):
    """
    Contains a reference to a single 'image' dataset, can be N-dimensional so
    covers 1D spectra, as well as 3D cubes and 4D hypercubes .
    The application should know the type (fits, casa image, miriad, nemo, ....)
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"IMAGE", filename, filetype)
        # cubes are written as [nx,ny,nz]
        # do we really need meta data here, isn't the filename enough?
        self.dims=[]

class BDP_table(BDP):
    """
    Contains a reference to one or more tables
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"TABLE", filename, filetype)
        self.table = []

class BDP_cubestats(BDP):
    """
    Contains a reference to a cubestats table
    channel, frequency, mean, sigma, max, [maxposx, maxposy]
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"CUBESTATS", filename, filetype)
        self.table = None
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
    frequency, data
    """
    def __init__(self, filename=None, filetype=None):
        BDP.__init__(self,"CUBESPECTRUM", filename, filetype)
        self.table = []
    def set_table(self,t):
        self.table = t
    def get_table(self):
        return self.table

#
# ==============================================================================

class AT(object):
    taskid  = 0                   # static AT class counter of the ATI's
    env     = 'casa'
    name    = 'base class'
    version = '1.0'
    keys    = []
    def __init__(self,name):
        if _debug: print "AT(%s)" % (name)
        self.taskid = AT.taskid
        AT.taskid = AT.taskid + 1
        self.name      = name
        self.do_pickle = True
        self.do_plot   = True
        self.updated   = None     # deprecated    # or should the FlowManager keep track of this?
        self.stale     = True     # if stale, it will trigger a new run 
        self.enable    = True     # disable/enable flow portions explicitly
        
        self.bdp_in    = []       # will be contructed during the admit.add()
        self.bdp_out   = []       # will be created during the AT_xxx() constructor
        self.keyvals   = {}       # the state of the keywords for this AT
        self.pmode     = 0        # plot mode
    def __len__(self):
        return len(self.bdp_out)
    def len2(self):
        return (len(self.bdp_in), len(self.bdp_out))
    def __getitem__(self,index):
        if index >= len(self.bdp_out):
            print "AT::%s has bdp len %d,%d" % (self.name,len(self.bdp_in),len(self.bdp_out))
        return self.bdp_out[index]
    def show(self):
        return self.name
    def check(self):
        print "No AT.check() in baseclase for %s" % self.name
    def run(self):
        """ run the task, but the only thing this returns is a True or False
        to designate if the AT was up to date.  Returns True if the real
        AT_xxx needs to run.
        """
        # if _debug: print "AT.run(%s)" % self.name
        os.system('echo -n AT_DATE=%s=; date' % self.name)
        if self.enable and self.stale:
            return True
        return False
    def setenv(self,newval):
        # playing with env
        self.env = newval
    def getenv(self):
        # why is env not available
        return self.env
    def set(self,keyvals):
        """
        Usage: set("key=val")
        perhaps allow  set([]) as well
        """
        kv = keyvals.split('=')
        if kv[0] in self.keys:
            self.setkv({ kv[0] : kv[1] })
        else:
            print "*** Skipped keyval ",keyvals," for ",self.name
    def setkv(self,keyvals):
        """set a task parameter"""
        # store them, but should also check if valid
        #print "set keys: ",self.keys
        for k in keyvals.keys():
            self.keyvals[k] = keyvals[k]
        self.stale = True
    def mgeti(self, key, default=None):
        ss = self.get(key,default).split(',')
        si = []
        for s in ss:
            si.append(int(s))
        return si
    def mgetf(self, key, default=None):
        ss = self.get(key,default).split(',')
        si = []
        for s in ss:
            si.append(float(s))
        return si
    def geti(self, key, default=None):
        """parse and return as integer"""
        return int(self.get(key,default))
    def getf(self, key, default=None):
        """parse and return as float"""
        return float(self.get(key,default))
    def getb(self, key, default=None):
        """parse and return as boolean (0=false 1=true)"""
        b = int(self.get(key,default))
        if b==0: return False
        return True
    def get(self, key, default=None):
        if default == None:
            if self.has(key):
                return self.keyvals[key]
            else:
                # bad
                print "No value for key ",key
                return ""
        else:
            if self.has(key):
                return self.keyvals[key]
            else:
                return default
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
    def __init__(self):
        AT.__init__(self,self.name)
    def run(self):
        if not AT.run(self): return False
        # do your work:
        #     self.bdp_in[] and self.bdp_out[] contain BDP's 
        #     ... contain parameters

class AT_file(AT):
    """ Create a simple container for a file, with no further description.

        bdp_in[]:    none
        bdp_out[0]:  filename
    """
    name    = 'FILE'
    version = '1.0'
    keys    = ['file','touch']
    def __init__(self,name=None):
        if name != None: self.name = name
        AT.__init__(self,self.name)
        if _debug: print "AT_file.init"
        self.bdp_out = [BDP_file(self.name)]
    def check(self):
        if _debug: print "CHECK AT_file"
    def run(self):
        if _debug: print "AT_file.run"
        if not AT.run(self): return False
        if self.getb('touch',1):
            fn = self.bdp_out[0].filename
            print "TOUCHING",fn
            os.system('touch %s' % fn)
        #


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
        if not AT.run(self): return False
        # specialized work can commence here


# the classes below are for playing with pipelines, they do no real work.
#
# flow:   1 -> 1
# flow12: 1 -> 2
# flow21: 2 -> 1
# flow1N: 1 -> N 
# flowN1: N -> 1
#

class AT_flow(AT):
    """ change one BDP into another one"""
    name = 'FLOW'
    version = '1.0'
    keys = ['debug','touch']
    def __init__(self,name=None):
        if name != None: self.name = name
        if _debug: print "AT_flow.init"
        AT.__init__(self,self.name)

        b = BDP_file(self.name)
        self.bdp_out = [b]
    def run(self):
        if _debug: print "AT_flow.run(%s)" % self.name
        if not AT.run(self): return False
        print "  work_flow: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        if self.getb('touch',1):
            fn = self.bdp_out[0].filename
            print "TOUCHING",fn
            os.system('touch %s' % fn)
        #
        if self.do_pickle:
            self.pdump()
  

class AT_flow12(AT):
    """ split one BDP into two """
    name = 'FLOW12'
    version = '1.0'
    keys = ['debug','touch']
    def __init__(self,name=None):
        if name != None: self.name = name
        if _debug: print "AT_flow12.init"
        AT.__init__(self,self.name)
        b1 = BDP_file(self.name + '.1')
        b2 = BDP_file(self.name + '.2')
        self.bdp_out = [b1,b2]
    def run(self):
        if _debug: print "AT_flow12.run(%s)" % self.name
        if not AT.run(self): return False
        # specialized work can commence here
        print "  work_flow12: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        if self.getb('touch',1):
            for i in [0,1]:
                fn = self.bdp_out[i].filename
                print "TOUCHING",fn
                os.system('touch %s' % fn)
        if self.do_pickle:
            self.pdump()

class AT_flow21(AT):
    """ combine two BDPs into one"""
    name = 'FLOW21'
    version = '1.0'
    keys = ['debug','touch']
    def __init__(self,name=None):
        if name != None: self.name = name
        AT.__init__(self,self.name)
        if _debug: print "AT_flow21.init"
    def check(self):
        b = BDP_file(self.name)
        self.bdp_out = [b]
    def run(self):
        if _debug: print "AT_flow21.run(%s)" % self.name
        if not AT.run(self): return False
        # specialized work can commence here
        print "  work: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        print "  in:  ",self.bdp_in[0].show(),self.bdp_in[1].show()
        print "  out: ",self.bdp_out[0].show()
        if self.getb('touch',1):
            fn = self.bdp_out[0].filename
            print "TOUCHING",fn
            os.system('touch %s' % fn)
        if self.do_pickle:
            self.pdump()

class AT_flow22(AT):
    """ arrange two BDPs into two others"""
    name = 'FLOW22'
    version = '1.0'
    keys = ['debug']
    def __init__(self,name=None):
        if name != None: self.name = name
        AT.__init__(self,self.name)
        if _debug: print "AT_flow22.init"
    def check(self):
        b1 = BDP_file(self.name + '.1')
        b2 = BDP_file(self.name + '.2')
        self.bdp_out = [b1,b2]
    def run(self):
        if _debug: print "AT_flow22.run(%s)" % self.name
        if not AT.run(self): return False
        # specialized work can commence here
        print "  work: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        print "  in:  ",self.bdp_in[0].show(),self.bdp_in[1].show()
        print "  out: ",self.bdp_out[0].show(),self.bdp_out[1].show()
        if self.do_pickle:
            self.pdump()

class AT_flow1N(AT):
    """Split one BDP into N BDPs.  The value of N is perhaps not known before entry, but this
    differs how the AT should handle this:
    1) caller knows N and allocates the array bdp_out[] and the AT fills them
    2) caller does not know N (e.g. it depends on the bdp_in[] and keys[]), and 
       can give either an empty bdp[] or a single [b] , the AT will then allocate
       and add to this list. This however means that the AT needs to make decisions
       on naming convention, in either case.
    """
    name = 'FLOW1N'
    version = '1.0'
    keys = ['n','debug','touch']
    def __init__(self,name=None):
        if name != None: self.name = name
        if _debug: print "AT_flow1N.init"
        AT.__init__(self,self.name)
        # note we cannot allocate BDP's because we don't know N yet
        # thus the run() task will need to broadcast the information
        # for admit to pick this up
        # but....
        # bdp_in set in a.add()
        # bdp_out set in constructor (normally)
    def check(self):
        print "CHECK AT_flow1N "
        n = self.geti('n',0)
        if n > 0:
            b=[]
            for i in range(n):
                b.append(BDP_file(self.name+'.%d'%(i+1)))
            self.bdp_out = b
    def run(self):
        if _debug: print "AT_flow1N.run(%s)" % self.name
        if not AT.run(self): return False
        # specialized work can commence here

        # simulate that N wasn't known until run-time, by setting it to < N
        n = self.geti('n',0)
        if len(self.bdp_out)==0:
            if n < 0:
                n = -n
                b=[]
                for i in range(n):
                    b.append(BDP_file(self.name+'.%d'%(i+1)))
                self.bdp_out = b             
        print "  work_flow1N: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        if self.getb('touch',1):
            for i in range(n):
                fn = self.bdp_out[i].filename
                print "TOUCHING",fn
                os.system('touch %s' % fn)

        if self.do_pickle:
            self.pdump()

class AT_flowN1(AT):
    """Take BDPs, merge them into one"""
    name = 'FLOWN1'
    version = '1.0'
    keys = ['debug','touch']
    def __init__(self,name=None):
        if name != None: self.name = name
        if _debug: print "AT_flowN1.init"
        AT.__init__(self,self.name)
    def check(self):
        #
        if _debug: print 'check'
    def run(self):
        if _debug: print "AT_flowN1.run(%s)" % self.name
        if not AT.run(self): return False
        # specialized work can commence here
        b = [BDP_file(self.name)]
        self.bdp_out = b
        print "  work_flowN1: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        if self.getb('touch',1):
            fn = self.bdp_out[0].filename
            print "TOUCHING",fn
            os.system('touch %s' % fn)      
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
