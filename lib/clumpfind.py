#! /usr/bin/env python
#
#  clumpfind wrapper (cf. the 3 in 1 Adam Leroy wrote)
#

import sys
import runidl
import runsh

class ClumpFind(object):
    """
    Valid names are
    mir::clfind
    idl::clfind (or gdl)
    idl::cprops (or gdl)
    """
    def __init__(self,name='mir::clfind'):
        self.name = name
        self.valid = []
        self.register('mir::clfind')
        self.register('idl::clfind')
        self.register('idl::cprops')
    def myname(self):
        return self.name
    def register(self,name):
        self.valid.append(name)
    def runtest1(self,find=True,stats=True):
        x = runidl.IDL()
        if find:
            cmd=[]
            cmd.append(".run clfind")
            cmd.append("clfind,file='../data/ros13co',low=0.5,inc=0.5,/log")
            x.run(cmd)
        if stats:
            cmd=[]
            cmd.append(".run clstats")
            cmd.append("clstats,file='../data/ros13co',/log")
            x.run(cmd)
        # should see 105 clumps
    def runtest2(self,find=True,stats=True):
        print "You might need: fits in=ros13co.fits out=ros13co.mir op=xyin"
        print "Also note old .cf file not cleaned up"
        fin='in=../data/ros13co.mir'
        x = runsh.shell()
        if find:
            cmd=['clfind',fin,'dt=0.5','start=1','nmin=4']
            x.run(cmd)
        if stats:
            cmd=['clstats',fin,'dist=1600','x=4.4','xy=abs']
            x.run(cmd)
        # should see 95 clumps
    
if __name__ == "__main__":
    # testing
    cf = ClumpFind()
    if sys.argv[1] == 'idl':
        cf.runtest1()
    if sys.argv[1] == 'mir':
        cf.runtest2()


