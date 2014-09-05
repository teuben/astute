import sys, os
import atable
import numpy as np
import admit1 as admit
#import casa
import taskinit

class AT_moments(admit.AT):
    name = 'MOMENTS'
    version = '1.0'
    keys = ['moments']
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
        fni = self.bdp_in[0].filename
        n1 = len(self.bdp_out)
        n2 = len(moments)
        if n1 != n2:
            print "%d bdp's and %d moments. bad" % (n1,n2)
            return
        # includepix=
        #  casa.immoments() doesn't have the overwrite option
        taskinit.ia.open(fni)
        for (m,b) in zip(moments,self.bdp_out):
            fno = b.filename
            taskinit.ia.moments(m,outfile=fno,overwrite=True)
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print "nothing to print here yet"
