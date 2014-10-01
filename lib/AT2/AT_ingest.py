import sys, os
import atable
import numpy as np
#import casa
import taskinit
import admit2 as admit

class AT_ingest(admit.AT):
    name = 'INGEST'
    version = '1.0'
    keys = ['mask','file','skip']
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        self.bdp_out = [  admit.BDP_file(self.name) ]
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        skip = self.geti('skip',0)
        create_mask = self.getb('mask',0)
        fni = self.get('file')
        fno = self.bdp_out[0].filename
        if skip: return

        print "casa::ia.fromfits(%s)" % fni
        taskinit.ia.fromfits(fno,fni,overwrite=True)
        if create_mask:
            # one of the egnog cubes has 1 bad plane
            # but this fails on n253 cubes (nan on the statistics)
            print "casa::ia.calcmask"
            taskinit.ia.calcmask('"%s" != 0.0' % fno)
        s = taskinit.ia.summary()
        s0 = taskinit.ia.statistics()
        print 'BASICS: ', s['shape'],s0['npts'],s0['min'],s0['max']
        taskinit.ia.close()
