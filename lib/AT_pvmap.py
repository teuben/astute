import sys, os
import atable
import numpy as np
import numpy.ma as ma
import casa
import taskinit
import admit1 as admit
import matplotlib.pyplot as plt


class AT_pvmap(admit.AT):
    name = 'PVMAP'
    version = '1.0'
    keys = ['start','end','width']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        #
        fni = self.bdp_in[0].filename    # input cube
        fno = self.bdp_out[0].filename   # output PV map
        print "casa::impv(%s)" % fin
        start = self.get('start')
        end   = self.get('end')
        width = self.get('width')
        h = casa.impv(fni,fno,start,end,width,overwrite=True)
        #
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            # should make a PV png
