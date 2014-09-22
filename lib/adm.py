#! /usr/bin/env python
#
#  various functions related to looping over directories
#  reading parameters etc. Precurser to ADMIT
#
#  adm = admit.ADMIT()
#

import parfile       as p
import admit.parfile as pp
import sys, os, errno, fnmatch

try:
    import pyfits
    print "pyfits loaded"
except:
    print "Warning: no pyfits found for this python"


try:
    import analysis_scripts.analysisUtils as au
    print "analysisUtils loaded"
except:
    print "Warning: analysisUtils could not be loaded"

try:
    import astropy
    print "astropy loaded"
except:
    print "Warning: astropy could not be loaded"

__version__ = "pre-ADMIT functions: $Id$"

__message__ = "wed 1410"


class ADMIT(object):
    """
    This is ADMIT
    """
    def __init__(self,name='',debug=True):
        self.parfile = "tas.def"
        self.debug   = debug
        self.name    = name
        if self.debug: print "ADMIT::init (%s)" % __message__
    def set_parfile(self,parfile):
        self.parfile = parfile
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
    def test(self,name='test'):
        a = ADMIT(name)
        return a

if __name__ == '__main__':
    print "No __main__ yet, if ever...."
