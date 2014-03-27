#
#    this test is really only meant for bench1
#    it needs the old-style tas.def from ASTUTE
#
import os
import admit.adm  as admit
import admit.parfile as parfile
import pyfits
import numpy    as np
import numpy.ma as ma

a=admit.ADMIT()

a.setdir('data/bench2')



for d in a.query_dir():
    a.setdir(d)
    p = parfile.ParFile('tas.def')
    fits = p.get('fits')
    print 'Fitsfile: ',fits
    if True:
        hdu = pyfits.open(os.path.expandvars(fits))
        data = hdu[0].data
        print 'data shape: ', data.shape
        dmin = data.min()
        dmax = data.max()
        print 'data           min/max: ',dmin,dmax
        m = ma.masked_array(data, np.isnan(data))
        print 'data (non NaN) min/max: ',m.min(), m.max()
    a.tesdir()


