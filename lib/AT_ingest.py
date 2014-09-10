import sys, os
import atable
import numpy as np
#import casa
import taskinit
import admit1 as admit

class AT_ingest(admit.AT):
    name = 'INGEST'
    version = '1.0'
    keys = ['mask']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        create_mask = True
        fni = self.bdp_in[0].filename
        fno = self.bdp_out[0].filename
        print "casa::ia.fromfits(%s)" % fni
        taskinit.ia.fromfits(fno,fni,overwrite=True)
        if create_mask:
            print "casa::ia.calcmask"
            taskinit.ia.calcmask('"%s" != 0.0' % fno)
        s = taskinit.ia.summary()
        s0 = taskinit.ia.statistics()
        print 'SHAPE: ', s['shape'],s0['npts']
        taskinit.ia.close()
