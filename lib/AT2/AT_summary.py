import sys, os
import atable
import numpy as np
import casa
import taskinit
import admit2 as admit

class AT_summary(admit.AT):
    name = 'SUMMARY'
    version = '1.0'
    keys = ['verbose']
    def __init__(self, name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        self.bdp_out = [  admit.BDP_summary(self.name) ]
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        fni = self.bdp_in[0].filename
        fno = self.bdp_out[0].filename
        #
        #
        verbose = self.geti('verbose',0)
        #
        taskinit.ia.open(fni)
        s = taskinit.ia.summary()
        if verbose:
            print s
        print '============================================================================'
        print 'AXIS',s['axisnames']
        print 'UNIT',s['axisunits']
        print 'SHAP',s['shape']
        print 'INCR',s['incr']
        print 'BMAJ',s['restoringbeam']['major']
        print 'COOR',s['refval']
        print '============================================================================'
        # just save a few for now, should be a formal container, not data{}
        for i in ['shape', 'refval', 'incr']:
            self.bdp_out[0].data[i] = s[i]
        if self.do_pickle:
            self.pdump()
