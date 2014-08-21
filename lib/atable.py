#! /usr/bin/env python
#
#  simple table class
#


import sys, os
import numpy as np
#import pickle
import cPickle as pickle

class ATable(object):
    """
    simple admit table
    """
    def __init__(self,cols=[],names=[],types=[],units=[]):
        self.n       = 0
        self.version = "20-aug-2014"
        self.cols    = cols
        self.names   = names
        self.types   = types
        self.units   = units
    def show(self):
        print 'names: ',self.names
        print 'types: ',self.types
        print 'units: ',self.units
    def get(self,name):
        for i in range(len(self.cols)):
            if name == self.names[i]:
                return self.cols[i]
    def pdump(self,filename):
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
    a.pdump("a.bin")
    b = a.pload("a.bin")
    print b.get('x')[0],b.get('y')[0],b.get('z')[0]

