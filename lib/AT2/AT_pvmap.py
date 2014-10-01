import sys, os
import atable, aplot
import numpy as np
import numpy.ma as ma
import admit2 as admit
import matplotlib.pyplot as plt
#
import casa, taskinit
from impv import impv


class AT_pvmap(admit.AT):
    """ PV map generated in one of many ways
    1) from a begin=, end=, width=
    2) from a PPP table, using moments of inertia. Needs a cutoff.
    3) from a CubeSum map, using moments of inertia. Needs a cutoff.
    """
    name = 'PVMAP'
    version = '1.0'
    keys = ['start','end','width','cutoff']
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        self.bdp_out = [ admit.BDP_image(self.name) ]
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        #
        nfni = len(self.bdp_in)
        if nfni == 1:
            # just an input cube, we need the start,end,width
            print "Only one input file"
        elif nfni == 2:
            # input can be an CubeSum image or CubeStats table with [maxposx,maxposy,max] 
            print 'input cube: ',self.bdp_in[0].name
            print 'helper file: ',self.bdp_in[1].name
        else:
            print "Not supported, falling back to start/end/width"
            
        fni = self.bdp_in[0].filename    # input cube
        fno = self.bdp_out[0].filename   # output PV map
        print "casa::impv(%s)" % fni
        # get the slice in P-P space
        # currently this matches the interface to IMPV, but a XCENTER,YCENTER,PA,LENGTH is also a useful 
        start = self.mgeti('start')
        end   = self.mgeti('end')
        width = self.geti('width',1)
        if False:
            # another case where this is not accessible via casa
            h = casa.impv(fni,fno,start,end,width,overwrite=True)
        else:
            h = impv(fni,fno,start,end,width,overwrite=True)
        #
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            # should make a PV png
            print "AT_pvmap: no plot yet"
