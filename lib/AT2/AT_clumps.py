import sys, os
import atable, aplot
import numpy as np
import admit2 as admit
import casa
import taskinit

class AT_clumps(admit.AT):
    """
    Input BDP:   0=mom0
                 1=mom1
                 2=mom2
    
    Output BDP:  table with clump properties

    Input also needs a series of positions, which are probed for intensity, velocity and linewidth
    for further analysis. The input positions will need to be obtained by other means.
    Interface to gather them is still clumsy because of the AT.set("keyword=value") string interface.
    """
    name = 'CLUMPS'
    version = '1.0'
    keys = ['region']
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        self.bdp_out = [ admit.BDP_table(self.name) ]
    def run(self):
        if not admit.AT.run(self):
            return False
        if len(self.bdp_in) != 3:
            print "len=%d" % len(self.bdp_in)
            print "Need 3 input file (mom0,1,2)"
        # specialized work can commence here
        b0 = self.bdp_in[0].filename
        b1 = self.bdp_in[1].filename
        b2 = self.bdp_in[2].filename
        flux=[]
        vlsr=[]
        disp=[]
        # should use mget()
        regions = self.get('region').split('\n')
        print 'REGIONS=',regions
        for (r,cn) in zip(regions,range(len(regions))):
            h0 = casa.imstat(b0,region=r)
            h1 = casa.imstat(b1,region=r)
            h2 = casa.imstat(b2,region=r)
            print "NPTS",h0['npts']
            if len(h0['npts']) > 0:
                flux.append(h0['flux'][0])
                vlsr.append(h1['mean'][0])
                disp.append(h2['mean'][0])
            else:
                flux.append(0.0)
                vlsr.append(0.0)
                disp.append(0.0)
            # no table yet, just ascii output here
            print 'CLUMPS',b0,(cn+1),flux[-1],vlsr[-1],disp[-1]
        #
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            # 
            print "AT_clumps: no plots"
