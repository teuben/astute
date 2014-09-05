#! /usr/bin/env python
#
#  simple table class
#


import sys, os
import numpy as np
import matplotlib.pyplot as plt
#import pickle
import cPickle as pickle

class ATable(object):
    """
    simple admit table
    """
    def __init__(self,cols=[],names=[],types=[],units=[],filename=None):
        self.n       = 0
        self.version = "2-sep-2014"
        self.cols    = cols
        self.names   = names
        self.types   = types
        self.units   = units
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
        
    def get(self,name):
        for i in range(len(self.cols)):
            if name == self.names[i]:
                return self.cols[i]
    def plotter(self,x,y,title=None,figname=None,xlab=None,ylab=None):
        """simple plotter of multiple columns against one column"""
        # if filename: plt.ion()
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        for yi in y:
            ax1.plot(x,yi)
        if title:    ax1.set_title(title)
        if xlab:     ax1.set_xlabel(xlab)
        if ylab:     ax1.set_ylabel(ylab)
        if figname: fig.savefig(figname)
        plt.show()
    def histogram(self,x,title=None,figname=None,xlab=None,range=None,bins=80):
        """simple histogram of one or more columns """
        # if filename: plt.ion()
        fig = plt.figure()
        ax1 = fig.add_subplot(1,1,1)
        for xi in x:
            if range:
                ax1.hist(xi,bins=bins,range=range)
            else:
                ax1.hist(xi,bins=bins)
        if title:    ax1.set_title(title)
        if xlab:     ax1.set_xlabel(xlab)
        if figname: fig.savefig(figname)
        plt.show()
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

