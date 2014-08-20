#! /usr/bin/env python
#
#  Initialize various useful tihngs for ASTUTE
#
#  1) find out what environment we have and what packages we have
#  2) provide easy interfaces to run alien packages (shell, idl)


import sys, os
import numpy as np
#import pickle
import cPickle as pickle

class ATable(object):
    """
    admit table
    """
    def __init__(self,cols,names):
        self.n       = 0
        self.version = "19-aug-2014"
        self.cols    = cols
        self.names   = names
    def show(self):
        print self.names
    def get(self,name):
        for i in range(len(self.cols)):
            if name == self.names[i]:
                return self.cols[i]
    def psave(self,filename):
        pickle.dump(self,open(filename,"wb"))
    def pload(self,filename):
        return pickle.load(open(filename,"rb"))
            
if __name__ == "__main__":
    x = np.arange(0,1,0.1)
    y = x*x
    z = x + y
    a = ATable([x,y,z],['x','y','z'])
    a.show()
    a1 = a.get('x')
    a1[0] = 999.9
    a.get('y')[0] = -1.0
    print x[0],y[0],z[0]
    print a.get('x')[0],a.get('y')[0],a.get('z')[0]
    pickle.dump(a,open("a.bin","wb"))
    b = pickle.load(open( "a.bin", "rb" ))
    print b.get('x')[0],b.get('y')[0],b.get('z')[0]


