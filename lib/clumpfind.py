#! /usr/bin/env python
#
#  clumpfinders
## >> .run clfind
# >> clfind,file='../example/rosette',low=0.5,inc=0.5,/log

import sys
import runidl

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
        print self.valid
    def runtest(self):
        x = runidl.IDL()
        cmd=[]
        cmd.append(".run clfind")
        cmd.append("clfind,file='../data/ros13co',low=0.5,inc=0.5,/log")
        x.run(cmd)
    

if __name__ == "__main__":
    # testing
    cf = ClumpFind()
    cf.runtest()
    


