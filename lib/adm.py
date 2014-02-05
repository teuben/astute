#! /usr/bin/env python
#
#  various functions related to looping over directories
#  reading parameters etc. Precurser to ADMIT
#
#  adm = admit.ADMIT()

import parfile as p
import sys, os

__version__ = "pre-ADMIT functions: $Id$"


class ADMIT(object):
    def __init__(self):
        print "ADM init"
        self.parfile = "tas.def"
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
        for path, dirs, files in os.walk(path):
            for f in files:
                if f == self.parfile: dlist.append(path)
        return dlist
    def setdir(self,dirname):
        """
        change directory to dirname to work in. Assumed to contain parameter file
        """
        self.p = dirname
        os.chdir(dirname)

if __name__ == '__main__':
    print "No __main__ yet, if ever...."
