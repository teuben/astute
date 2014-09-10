import sys, os
import atable
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import admit1 as admit
#import casa
import taskinit

def line_segments(data,cut,nline,ngap,ngrow=0):
    """
    find segments that define a line
    [ [start1,end1], [start2,end2], ....]
    ngrow: not implemented
    """
    def index(w,start,value):
        n = len(w)
        i = start
        while i < n:
            if w[i] == value: return i
            i = i + 1
        return -1
    def setval(w,start,end,value):
        for i in range(start,end):
            w[i] = value
    print "data range: ",data.min(),data.max()
    print "cut: ",cut
    print "nline: ",nline
    print "ngap: ",ngap
    s = []
    n = len(data)
    # dw = ma.masked_less(d,cut)
    w = range(n)
    for i in range(n):
        if data[i] < cut:
            w[i] = 0
        else:
            w[i] = 1
    #
    i0 = 0
    while i0 >= 0:
        i1 = index(w,i0,1)
        if i1<0: break
        i2 = index(w,i1,0)
        if i2<0: break
        i3 = index(w,i2,1)
        if i3<0: break
        #
        ig = i3-i2
        if ig <= ngap:
            # fill the gap, it's small
            setval(w,i2,i3,1)
            i0 = i1
            continue
        else:
            il = i2-i1
            if il >= nline:
                s.append([i1,i2])
            i0 = i2
            continue
    #
    return s
    

def robust(data,f=1.5):
    median = np.median(data)
    n = len(data)
    d = np.sort(data)
    n1 = n/4
    n2 = n/2
    n3 = (3*n)/4
    q1 = d[n1]
    q2 = d[n2]
    q3 = d[n3]
    d = q3-q1
    f1 = q1-f*d
    f3 = q3+f*d
    print "Median: ", median
    print "Q1,2,3:",q1,q2,q3
    print "f1,f3:",f1,f3
    dm = ma.masked_outside(data,f1,f3)
    return dm




def hisplot(x,title=None,figname=None,xlab=None,range=None,bins=80,gauss=None):
    """simple histogram of one or more columns """
    # if filename: plt.ion()
    fig = plt.figure(1)
    ax1 = fig.add_subplot(1,1,1)
    if range:
        ax1.hist(x,bins=bins,range=range)
    else:
        ax1.hist(x,bins=bins)
    if title:    ax1.set_title(title)
    if xlab:     ax1.set_xlabel(xlab)
    if gauss:
        a = 40.0
        m = gauss[0]
        s = gauss[1]
        d = s/20
        gx = np.arange(x.min(),x.max(),d)
        arg = (gx-m)/s
        gy = a * np.exp(-0.5*arg*arg)
        ax1.plot(gx,gy)
    if figname: 
        fig.savefig(figname)
    plt.show()

class AT_linecube(admit.AT):
    """
    bdp_in[0]   bandcube
    bdp_in[1]   cubestats (needs cols::frequency,sigma,max)
    
    f       robustness parameter [1.5]
    cut1    signal above cutoff, rmean+cut1*rstd, is taken as line [2]
    ngap    allowed channels with signal below cutoff [0]
    nline   minimum number of channels needed for a line [3]
    """
    name = 'LINECUBE'
    version = '1.0'
    keys = ['f', 'cut1']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def plotter(self,x,y,title=None,figname=None,xlab=None,ylab=None,segments=None):
        """simple plotter of multiple columns against one column
           stolen from atable, allowing some extra bars in the plot
           for line_id
        """
        # if filename: plt.ion()
        #plt.ion()
        plt.ioff()
        fig = plt.figure()
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
        plt.show()
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        f = 1.5
        cut1 = 2.0
        ngap = 2
        nline = 3
        #
        fni = self.bdp_in[0].filename
        t = self.bdp_in[1].table
        freq  = t.get('frequency')
        sigma = t.get('sigma')
        peak  = t.get('max')
        ratio = np.log10(peak)-np.log10(sigma)
        dr = robust(ratio,f)
        print "ROBUST:",dr.mean(), ma.median(dr), dr.std()
        ratio2 = dr.compressed()
        cutoff = dr.mean() + cut1*dr.std()
        segments = line_segments(ratio,cutoff,nline,ngap)
        print "Found %d lines" % len(segments)
        print segments
        segp = []
        n = len(freq)
        rmax = ratio.max() #  + 0.05*(ratio.max()-ratio.min())
        segp.append(  [freq[0],freq[n-1],cutoff,cutoff] )
        for s in segments:
            ch0 = s[0]
            ch1 = s[1]
            print "Cutting a cube %d - %d" % (ch0,ch1)
            segp.append(  [freq[ch0],freq[ch1],rmax,rmax] )
        print segp
        

        #
        self.plotter(freq,[ratio],'LineCubeStats-1',xlab='Freq',ylab='log(signal/noise)',figname='linecube1.png',segments=segp)

        t.histogram([ratio,ratio2],'LineCubeStats-2',figname='linecube2.png')
        #
        hisplot(ratio,gauss=[dr.mean(),dr.std()])
        #


        taskinit.ia.open(fni)
        taskinit.ia.close()

        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print "nothing to print here yet"
