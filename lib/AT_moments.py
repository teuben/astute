import sys, os
import atable
import numpy as np
import admit1 as admit
import casa
import taskinit

class AT_moments(admit.AT):
    name = 'MOMENTS'
    version = '1.0'
    keys = ['moments','nsigma','cutoff']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        if self.has('moments'):
            # convert string to int's
            moments = []
            for m in self.get('moments').split(','):
                moments.append(int(m))
        else:
            moments = [0]
        #
        cutoff = self.getf('cutoff')
        dmax = 999999.9
        fni = self.bdp_in[0].filename
        n1 = len(self.bdp_out)
        n2 = len(moments)
        if n1 != n2:
            print "%d bdp's and %d moments. bad" % (n1,n2)
            return
        #  includepix=
        #  casa.immoments() doesn't have the overwrite option
        taskinit.ia.open(fni)
        for (m,b) in zip(moments,self.bdp_out):
            fno = b.filename
            taskinit.ia.moments(m,outfile=fno,includepix=[cutoff,dmax],overwrite=True)
            b.moment = m
            if m==0:
                fno0 = fno
                b0 = b
                # add the flux/sum to the header
                # 'sum' is the sum of the pixels, not beam corrected
                if True:
                    # @todo  CASA BUG ?
                    # something not working, if we don't do an extra "dummy" imstat on 'fni', the 'fno' doesn't work":
                    # SEVERE	imstat::ImageAnalysis::open	Image linecube.U-112.357.mom0 cannot be opened; its type is unknown
                    h = casa.imstat(fni)
                    h = casa.imstat(fno)
                    b.flux = h['sum']
        #
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print "nothing to print here yet"
