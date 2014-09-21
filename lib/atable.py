#! /usr/bin/env python
#
#  simple table class, for plotting, see aplot
#


import sys, os
import numpy as np
#import pickle
import cPickle as pickle

class ATable(object):
    """
    simple admit table
    """
    def __init__(self,cols=[],names=[],types=[],units=[],filename=None):
        self.n       = 0
        self.version = "17-sep-2014"
        self.cols    = cols
        self.names   = names
        self.types   = types
        self.units   = units
        self.fign    = 0
        if filename:
            # horrible shortcut
            # e.g.     atable.ATable(filename="cubestats.bin").show()
            t = pickle.load(open(filename,"rb"))
            self.cols  = t.cols
            self.names = t.names
            self.types = t.types
            self.units = t.units
    def show(self):
        print 'table: %d cols x %d rows' % (len(self.names),len(self.cols[0]))
        print 'col_names: ',self.names
        print 'col_types: ',self.types
        print 'col_units: ',self.units
    def data(self):
        """ just for debug, needs prettier output"""
        n = len(self.cols[0])
        m = len(self.cols)
        for i in range(n):
            d = []
            for j in range(m):
                d.append(self.cols[j][i])
            print d
    def get(self,name):
        for i in range(len(self.cols)):
            if name == self.names[i]:
                return self.cols[i]
    def pdump(self,filename):
        pickle.dump(self,open(filename,"wb"))
    def pload(self,filename):
        return pickle.load(open(filename,"rb"))
            
if __name__ == "__main__":
    def try1(t):
        x = np.arange(0,1,0.1)
        y = x*x
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
    #
    s1=['a','b','d','e']
    s2=[ 1 , 2 , 4 , 5 ]
    a2 = ATable([s1,s2],['s1','s2'],['string','int'])
    a2.show()
    a2.pdump('a2.bin')
    b2 = a.pload('a2.bin')
    s1[0] = 'z'
    print b2.cols
    print a2.cols

