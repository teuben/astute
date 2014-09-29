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

    pmin    not used now

    virtual = 0 or 1 (experimenting)

    linedir = 0 or 1 :    1 means every linecube gets its own directory

    A few words on virtual lineCubes.   The idea is that in principle you don't need to cut cubes and spend the
    diskspace. You could just record the restfreq and channel range, and when-ever programs need to work on a
    line cube, they peek into the spwCube.   This implementation was only tested here, although not really using
    the restfreq.

    """
    name = 'LINECUBE'
    version = '1.0'
    keys = ['pmin','virtual','linedir']
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
        pmin    = self.getf('pmin',1.0)
        virtual = self.getb('virtual',0)
        linedir = self.getb('linedir',0)
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
            chans = '%d~%d' % (ch0[l],ch1[l])
            if linedir:
                lname = "%s.%s" %  (fno,short[l])
                os.system('mkdir -p %s' % lname)
                lname = "%s/cim" % lname
            else:
                lname = "%s.%s" %  (fno,short[l])
            self.bdp_out.append(admit.BDP_image(lname))
            if not virtual:
                print "Cutting a CASA cube %s chans=%s @ %g GHz" % (lname,chans,freq[l])
                # @todo figure this out why casa.imsubimage doesn't work
                imsubimage(fni,lname,overwrite=True,chans=chans)
                self.bdp_out[l].virtual = 0
            else:
                print "Cutting a virtual cube %s chans=%s @ %g GHz" % (lname,chans,freq[l])
                b = self.bdp_out[l]
                b.virtual  = fni
                b.linecube = lname
                b.chan0    = ch0[l]
                b.chan1    = ch1[l]
                b.restfreq = freq[l]
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print 'AT_linecube: no plots'
