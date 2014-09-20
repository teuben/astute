import sys, os
import atable
import numpy as np
import numpy.ma as ma
import casa
import taskinit
import admit1 as admit
import matplotlib.pyplot as plt

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

def hisplot(x,title=None,figname=None,xlab=None,range=None,bins=80,gauss=None):
    """simple histogram of one or more columns """
    # if filename: plt.ion()
    # better example: http://matplotlib.org/examples/statistics/histogram_demo_features.htmlsparspark
    fig = plt.figure(1)
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
    plt.show()


class AT_cubesum(admit.AT):
    name = 'CUBESUM'
    version = '1.0'
    keys = ['nsigma','verbose','cutoff']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        #
        verbose      = self.geti('verbose',0)
        nsigma       = self.getf('nsigma',4)
        cutoff       = self.getf('cutoff',-1)
        #
        fni = self.bdp_in[0].filename     # input cube
        fno = self.bdp_out[0].filename    # output mom0
        dmax = 1e99                        # or get from cubestats
        if cutoff < 0:
            # what if we want to make mom0's of absorption features?
            sigma = self.bdp_in[1].sigma    # from cubestats
            cutoff = nsigma * sigma
        # 0.0013 4sigma = 
        # moment=0 or [0] ?
        # includepix=[0.005,]     # unexpected results
        # some typos in the help() file
        #
        # note: immoments has no overwrite= keyword
        os.system('rm -rf %s' % fno)
        casa.immoments(fni,moment=0,includepix=[cutoff,dmax],outfile=fno)

        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print 'No plotting in cubesum yet"
