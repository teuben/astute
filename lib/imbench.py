#! /usr/bin/env python
#
#  benchmarking some image I/O routines in various packages as function of size
#  IDL/GDL
#  python (numpy)
#  MIRIAD
#  NEMO
#


import sys
import runidl
import runsh
import pyfits


class ImBench(object):
    """
    Valid prefixes are
    mir::
    idl::
    nemo::
    """
    def __init__(self,name='mir::image',size=[100,100,100],file=None):
        print "ImBench %s[%d,%d,%d]" % (name,size[0],size[1],size[1])
        self.name = name
        self.valid = []
        self.register('mir::image')
        self.register('idl::image')
        self.register('nemo::image')
        self.register('numpy::image')
    def myname(self):
        return self.name
    def register(self,name):
        self.valid.append(name)

        
if __name__ == "__main__":
    # testing
    ib = ImBench()

