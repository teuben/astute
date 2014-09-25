import sys, os, math
import atable, aplot
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import admit2 as admit
#import casa
import taskinit


def rejecto1(data, f=1.5):
    u = np.mean(data)
    s = np.std(data)
    newdata = [e for e in data if (u - f * s < e < u + f * s)]
    return newdata

def rejecto2(data, f=1.5):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<f]

def mystats(data):
    m1 = data.mean()
    s1 = data.std()
    n1 = len(data)
    d = rejecto2(data)
    m2 = d.mean()
    s2 = d.std()
    n2 = len(d)
    return (n1,m1,s1,n2,m2,s2)


def line_segments(data,cutoff,nline,ngap,ngrow=0):
    """
    find segments that define a line
    [ [start1,end1], [start2,end2], ....]
    ngrow: not implemented

    could imagine nline smaller if the data-cutoff is
    bigger, i.e. narrower but stronger signals still
    get accepted
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
    print "cutoff: ",cutoff
    s = []
    n = len(data)
    # dw = ma.masked_less(d,cutoff)
    w = range(n)
    for i in range(n):
        if data[i] < cutoff:
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
        if i3<0: 
            il = i2-i1
            if il>= nline:
                s.append([i1,i2])
            break
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

class AT_linelist(admit.AT):
    """
    LINELIST:  should be called LINEID when it does the lineid
    bdp_in[0]   bandcube
    bdp_in[1]   cubestats (needs cols::frequency,sigma,max)
    
    f       robustness parameter [1.5]
    nsigma  signal above cutoff, rmean+nsigma*rstd, is taken as line [2]
    ngap    allowed channels with signal below cutoff [0]
    nline   minimum number of channels needed for a line [3]
    """
    name = 'LINELIST'
    version = '1.0'
    keys = ['f', 'nsigma', 'nline', 'ngap', 'csigma', 'vlsr']
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        self.bdp_out = [ admit.BDP_table(self.name) ]       
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        #
        f      = self.getf('f',1.5)
        nsigma = self.getf('nsigma',2.0)
        nline  = self.geti('nline',3)
        ngap   = self.geti('ngap',2)
        csigma = self.getf('csigma',2.0)
        vlsr   = self.getf('vlsr',0.0)
        #
        fni = self.bdp_in[0].filename
        t = self.bdp_in[1].table
        freq  = t.get('frequency')
        # @ todo:  relativistic
        if True:
            freq = freq/(1-vlsr/299792.458)
        sigma = t.get('sigma')
        peak  = t.get('max')
        ratio = np.log10(peak)-np.log10(sigma)
        dr = robust(ratio,f)
        print "ROBUST:",dr.mean(), ma.median(dr), dr.std()
        ratio2 = dr.compressed()
        dmean = dr.mean()
        cutoff = dmean + nsigma*dr.std()
        print "SEGMENTS: f=%g nsigma=%g ngap=%d nline=%d" % (f,nsigma,ngap,nline)
        segments = line_segments(ratio,cutoff,nline,ngap)
        nlines = len(segments)
        print "Found %d lines" % nlines
        # print segments
        segp = []
        n = len(freq)
        rmax = ratio.max() + 0.1 #  + 0.05*(ratio.max()-ratio.min())
        segp.append(  [freq[0],freq[n-1],cutoff,cutoff] )
        segp.append(  [freq[0],freq[n-1],dmean,dmean] )
        # allocate atable for BDP
        tfreq  = np.arange(nlines,dtype=float)     ; c1 = 'frequency'
        twidth = np.arange(nlines,dtype=float)     ; c2 = 'width'
        tshort = range(nlines)                     ; c3 = 'short'
        tlikel = np.arange(nlines,dtype=float)     ; c4 = 'likely'
        tfull  = range(nlines)                     ; c5 = 'long'
        tch0   = range(nlines)                     ; c6 = 'ch0'
        tch1   = range(nlines)                     ; c7 = 'ch1'
        for (l,s) in zip(range(nlines),segments):
            ch0 = s[0]
            ch1 = s[1]
            sum0 = sum(ratio[ch0:ch1])
            sum1 = sum(freq[ch0:ch1]*ratio[ch0:ch1])
            sum2 = sum(freq[ch0:ch1]*freq[ch0:ch1]*ratio[ch0:ch1])
            lmean  = sum1/sum0
            lsigma = math.sqrt(sum2/sum0-lmean*lmean)
            lmax  = max(ratio[ch0:ch1])
            print "Line in channels %d - %d  @ %g GHz +/- %g GHz log(S/N) = %g" % (ch0,ch1,lmean,lsigma,lmax)
            segp.append(  [freq[ch0],freq[ch1],rmax,rmax] )
            segp.append(  [lmean,lmean, rmax-0.1, rmax+0.05] )
            #
            lname = "U-%.3f" % lmean      # name of the line (not identified yet)
            tch0[l]   = ch0
            tch1[l]   = ch1
            tfreq[l]  = lmean
            twidth[l] = lsigma
            tlikel[l] = lmax
            tshort[l] = lname
            tfull[l]  = lname
        col_names = [c1,    c2,     c3,     c4,     c5,    c6,   c7]
        col_data  = [tfreq, twidth, tshort, tlikel, tfull, tch0, tch1]
        a1 = atable.ATable(col_data, col_names)
        a1.pdump('linelist.bin')
        self.bdp_out[0].table = a1
        # print segp
        if csigma > 0:
            taskinit.tb.open(fni)
            data = taskinit.tb.getcol('map')   # get the N-Dim view
            shape = data.shape
            taskinit.tb.close()
            d1 = data.ravel()                  # get a 1D view
            d1 = d1*1000.0                     # get it in mJy/beam
            (n1,m1,s1,n2,m2,s2) = mystats(d1)
            print 'MYSTATS',n1,m1,s1,n2,m2,s2
            cutoff2 = csigma*s2
            print 'cutoff2=',cutoff2
            # s2 should be a critical cutoff
            nx = shape[0]
            ny = shape[1]
            nz = shape[2]
            if shape[3] != 1:
                print "big fat warning: cannot deal with 4D cubes."
            if nz != len(freq):
                print "big far warning: freq[%d] and shape[][][%d] not same" % (len(freq),nz)
            csum = np.zeros(nz)
            for k in range(nz):
                sm0 = data[0:nx,0:ny,k,0]*1000
                sm1 = ma.masked_less(sm0,cutoff2)
                csum[k] = sm1.sum()
            aplot.APlot().plotter(freq,[csum],'CubeCut csigma=%g' % csigma,xlab='Freq',figname='linelist0.png')
            # now decide if 'csum' is going to be a column in cubestats

        #  ...trying out some plots....
        #  this needs to be streamlined
        #  e.g. the segp[], could add a macro processor to plotter/histogram
        #  accepting
        xlab = 'Frequency (Ghz) vlsr=%g' % vlsr
        ylab = 'log(Peak/Noise)'
        aplot.APlot().plotter2(freq,[ratio],'LineList-1',xlab=xlab,ylab=ylab,figname='linelist1.png',segments=segp)
        xlab = 'log(Peak/Noise)'
        aplot.APlot().histogram([ratio,ratio2],'LineList-2',figname='linelist2.png',xlab=xlab)
        xlab = 'log(Peak/Noise)'
        aplot.APlot().hisplot(ratio,'LineList-3',figname='linelist3.png',gauss=[dr.mean(),dr.std()],xlab=xlab)
        #
        # store in the BDP
        #
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print "nothing to print here yet"
