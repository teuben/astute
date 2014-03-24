#! /usr/bin/env python
#
#  various functions related to looping over directories
#  reading parameters etc. Precurser to ADMIT
#
#  adm = admit.ADMIT()
#

import parfile as p
import admit.parfile as pp
import sys, os

try:
    import pyfits
except:
    print "Warning: no pyfits found for this python"

__version__ = "pre-ADMIT functions: $Id$"

__message__ = "mon 1659"


class ADMIT(object):
    """
    This is ADMIT
    """
    def __init__(self):
        print "ADMIT init (%s)" % __message__
        self.parfile = "tas.def"
        self.debug   = True
    def set_parfile(self,parfile):
        self.parfile = parfile
    def query_dir(self,here=None):
        """
        from here, drill down and find directories in which parameter files exists
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
    def setdir(self,dirname):
        """
        change directory to dirname to work in. Assumed to contain parameter file
        """
        self.p = dirname
        self.pwd = os.getcwd()
        os.chdir(dirname)
    def tesdir(self):
        """
        revert back from previous setdir
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

if __name__ == '__main__':
    print "No __main__ yet, if ever...."
