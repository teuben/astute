"""
ADMIT pipeline
Basic Data Product (BDP) class

"""
import sys, os
import optparse
# import pyfits
# import scipy
import fileinput
import numpy as np

import casac
from astropy.table import Table

from telescope import TelescopeType as Type

__version__ = '$Revision$'

####### Base BDP class #########
class BDP:

    def __init__(self, telescope, perms):
        self.tele_name = telescope
        self.tele_obj = Type()
        self.tele_obj.setVal(telescope, perms)

    def getTele(self):
        return self.tele_name
 
    def printPerms(self):
        return self.tele_obj.report()
 
    def readXML(self):
        rw = XMLrw()
        print "In readXML of BDP class"
 
    def writeBDP():
        print "In writeBDP, Telescope = %d" % tele_type
 
    def writeBDPZip():
        print "In writeBDPZIP of BDP Telescope = %d" % tele_type

#####################################
class BDPCubeStats(BDP):
    """ Class for ContinnumMap """
 
    def __init__(self, tel, perms):
        BDP.__init__(self, tel, perms)

    def writeBDP():
        print "In writeBDP of BDPCubStats"
        ia = casac.casac.image()
        ia.open(in_fits)

        print "After import fits"
#         s = imstat(f_im,axes=[0,1],logfile='imstat.logfile',append=False)
#     
#         # strange we need to do it this way.. imstat::s doesn't have them, the logfile does
#         h = imhead(f_im,mode='list')
#         n = h['shape'][2]
#         p = h['crpix3']
#         d = h['cdelt3']
#         v = h['crval3']
#         ch = np.arange(n) + 1
#         fr = (ch-p-1)*d + v
#         t = Table([ ch, fr, s['rms'], s['sigma']], names=('#channel','frequency','rms','sigma'))
#         t.write('imstat.astropy.tab',format='ascii')

 
#####################################
class BDPMomentMap(BDP):
    """ Class for MomentMap """
 
    def __init__(self, tel, perms):
        BDP.__init__(self, tel, perms)
 
#####################################
class BDPPeakSpectrum(BDP):
    """ Class for PeakSectrum """

    def __init__(self, tel, perms):
        BDP.__init__(self, tel, perms)
 

#### Test ####
if __name__ == "__main__":

    usage = """usage: %prog [options] ..."""

    parser = optparse.OptionParser(usage=usage, version=__version__)
    parser.add_option('-l', '--log', type='string', help = 'output or log file', default=None)
    parser.add_option('-f', '--file', type='string', help = 'input image file with full path', default=None)
    opts, args = parser.parse_args()

    # check input parameters
    if opts.file is None:
        sys.exit('Please enter input fits and log name.')

    name = "ALMA"
    ids = [('project', '2012.1.01234.S'),('sous', 'A000_X01_X00'), ('gous', 'A000_X01_X01'), 
       ('mous', 'A000_X01_Xxx1'), ('spw', 'spw1')]

    bdp = BDPCubeStats(name, ids)
 
#     print "Telescope name:", bdp.getTele()
#     bdp.printPerms()

    ia = casac.casac.image()
    ia.open(opts.file)

    s = ia.statistics(axes=[0,1],logfile=opts.log,append=False)

    h = ia.miscinfo()
    print '\n--- Header ---------\n', h

    print '\n--- Summary---------\n', ia.summary()
    print '\n--- Shape ----------\n', ia.shape()
    ia.close()
    print "\nDone"
