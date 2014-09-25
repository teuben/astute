import sys, os, math
import atable
import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import admit2 as admit
import casa
#import taskinit
from imsubimage import imsubimage

# in km/s
# imsubimage(f_im,l_out,overwrite=True,chans="range=[%gkm/s,%gkm/s], restfreq=%gGHz" % (vcube[0],vcube[1],freq[i]))
# imreframe(l_out,restfreq='%gGHz' % freq[i])

class AT_linecube(admit.AT):
    """
    bdp_in[0]          bandcube
    bdp_in[1]          linelist (needs cols::frequency,....)
    
    bdp_out[]          linecube(s); not set till runtime
    """
    name = 'LINECUBE'
    version = '1.0'
    keys = ['pmin']
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        # cannot determine?
        n = 0
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        #
        pmin   = self.getf('pmin',1.0)
        #
        fni = self.bdp_in[0].filename
        t = self.bdp_in[1].table
        fno = self.name
        freq = t.get('frequency')
        ch0 = t.get('ch0')
        ch1 = t.get('ch1')
        short = t.get('short')
        nlines = len(freq)
        print "Found %d lines" % nlines
        for l in range(nlines):
            lname = "%s.%s" %  (fno,short[l])
            chans = '%d~%d' % (ch0[l],ch1[l])
            print "Cutting a cube %s chans=%s @ %g GHz" % (lname,chans,freq[l])
            self.bdp_out.append(admit.BDP_image(lname))
            # @todo figure this out why casa.imsubimage doesn't work
            imsubimage(fni,lname,overwrite=True,chans=chans)
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print "nothing to print here yet"
