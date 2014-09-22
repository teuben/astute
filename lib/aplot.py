#! /usr/bin/env python
#
#  simple ADMIT plotter; 
#    - keeps track of figure numbers
#    - plotmode (interactive, with saving before or after interaction etc.)
#      -1  no saving files, no interactive screens
#       0
#       1
#       2
#    - simple parser of extra layout commands on top of general style
#    - plotter, scatter or histogram
#  
#
#  line x0 y0 x1 y1 ...
#  point x0 y0 ...


import sys, os
import numpy as np
import matplotlib.pyplot as plt
#import pickle
#import admit1 as admit

class APlot(object):
    """
    simple admit plotter
    """
    # static members
    pmode = 1
    ptype = '.png'
    figno = 0
    #
    def __init__(self,pmode=None,figno=None):
        self.version = "21-sep-2014"
        if pmode!=None: APlot.pmode = pmode
        if figno!=None: APlot.figno = figno
    def show(self):
        print "APlot:  pmode=%d [%d] figno=%d [%d]" % (APlot.pmode, self.pmode, APlot.figno, self.figno)
    def plotmode(self,pmode=0):
        APlot.pmode = pmode
    def figure(self,figno=1):
        APlot.figno = figno-1
    def parse(self,plt,fig,ax,lines):
        for line in lines:
            if line=='grid':
                plt.grid()
            elif line=='axis equal':
                plt.axis('equal')
            else:
                print "Skipping unknown aplot command: %s" % line
    def scatter(self,x,y,title=None,figname=None,xlab=None,ylab=None,c=None,s=None,cmds=None):
        """simple plotter of multiple columns against one column"""
        # if filename: plt.ion()
        #plt.ion()
        plt.ioff()
        APlot.figno = APlot.figno + 1
        fig = plt.figure(APlot.figno)
        ax1 = fig.add_subplot(1,1,1)
        if c==None and s==None:
            ax1.scatter(x,y)
        elif c==None:
            ax1.scatter(x,y,s=s)
        elif s==None:
            ax1.scatter(x,y,c=c)
        else:
            ax1.scatter(x,y,c=c,s=s)
        if title:    ax1.set_title(title)
        if xlab:     ax1.set_xlabel(xlab)
        if ylab:     ax1.set_ylabel(ylab)
        if cmds != None:
              self.parse(plt,fig,ax1,cmds)
        if figname: 
            fig.savefig(figname)
        if APlot.pmode:
            plt.show()
    def plotter(self,x,y,title=None,figname=None,xlab=None,ylab=None):
        """simple plotter of multiple columns against one column"""
        # if filename: plt.ion()
        #plt.ion()
        plt.ioff()
        APlot.figno = APlot.figno + 1
        fig = plt.figure(APlot.figno)
        ax1 = fig.add_subplot(1,1,1)
        for yi in y:
            ax1.plot(x,yi)
        if title:    ax1.set_title(title)
        if xlab:     ax1.set_xlabel(xlab)
        if ylab:     ax1.set_ylabel(ylab)
        if figname: 
            fig.savefig(figname)
        if APlot.pmode:
            plt.show()
    def plotter2(self,x,y,title=None,figname=None,xlab=None,ylab=None,segments=None):
        """simple plotter of multiple columns against one column
           stolen from atable, allowing some extra bars in the plot
           for line_id
        """
        # if filename: plt.ion()
        #plt.ion()
        plt.ioff()
        APlot.figno = APlot.figno + 1
        fig = plt.figure(APlot.figno)
        ax1 = fig.add_subplot(1,1,1)
        for yi in y:
            ax1.plot(x,yi)
        if segments:
            for s in segments:
                ax1.plot([s[0],s[1]],[s[2],s[3]])
        if title:    ax1.set_title(title)
        if xlab:     ax1.set_xlabel(xlab)
        if ylab:     ax1.set_ylabel(ylab)
        if figname: 
            fig.savefig(figname)
        if APlot.pmode:
            plt.show()

    def histogram(self,x,title=None,figname=None,xlab=None,range=None,bins=80):
        """simple histogram of one or more columns """
        # if filename: plt.ion()
        APlot.figno = APlot.figno + 1
        fig = plt.figure(APlot.figno)
        ax1 = fig.add_subplot(1,1,1)
        for xi in x:
            if range==None:
                ax1.hist(xi,bins=bins)
            else:
                ax1.hist(xi,bins=bins,range=range)
        if title:    ax1.set_title(title)
        if xlab:     ax1.set_xlabel(xlab)
        ax1.set_ylabel("#")
        if figname: 
            fig.savefig(figname)
        if APlot.pmode:
            plt.show()

    def hisplot(self,x,title=None,figname=None,xlab=None,range=None,bins=80,gauss=None):
        """simple histogram of one or more columns """
        # if filename: plt.ion()
        # better example: http://matplotlib.org/examples/statistics/histogram_demo_features.htmlsparspark
        APlot.figno = APlot.figno + 1
        fig = plt.figure(APlot.figno)
        ax1 = fig.add_subplot(1,1,1)
        if range == None:
            h=ax1.hist(x,bins=bins)
        else:
            h=ax1.hist(x,bins=bins,range=range)
        if title:    ax1.set_title(title)
        if xlab:     ax1.set_xlabel(xlab)
        ax1.set_ylabel("#")
        if gauss != None:
            if len(gauss) == 3:
                m = gauss[0]    # mean
                s = gauss[1]    # std
                a = gauss[2]    # amp
            elif len(gauss) == 2:
                m = gauss[0]    # mean
                s = gauss[1]    # std
                a = max(h[0])   # match peak value in histogram
            else:
                print "bad bad gauss estimator"
            print "GaussPlot(%g,%g,%g)" % (m,s,a)
            d = s/10.0
            if range == None:
                gx = np.arange(x.min(),x.max(),d)
            else:
                gx = np.arange(range[0],range[1],d)
            arg = (gx-m)/s
            gy = a * np.exp(-0.5*arg*arg)
            ax1.plot(gx,gy)
        if figname: 
            fig.savefig(figname)
        if APlot.pmode:
            plt.show()

if __name__ == "__main__":
    x = np.arange(0,1,0.1)
    y = x*x
    z = y-x

    p = 0
    a1 = APlot(1,10)
    a1.plotter(x,[y])
    a1.plotter(x,[z])
    a1.plotter(x,[y,z])
    a1.show()

    a2 = APlot(1,20)
    a2.histogram([x,y])
    a2.plotter(x,[y])
    a2.show()
