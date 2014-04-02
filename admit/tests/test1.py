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


#   could also hardcode this for data/bench1, but now it's searching
d=a.query_dir()
if len(d) == 0:
    print "No datasets found"
    sys.exit(1)
a.walkdir(d)
os.chdir(d[0])


p = parfile.ParFile('tas.def')
fits = p.get('fits')
print 'Fitsfile: ',fits

hdu = pyfits.open(os.path.expandvars(fits))
data = hdu[0].data
print 'data shape: ', data.shape
dmin = data.min()
dmax = data.max()
print 'data[15,30,30]: ',data[15,30,30]

m = ma.masked_array(data, np.isnan(data))
print 'data (non NaN) min/max: ',m.min(), m.max()
 
if False:
    am = np.ma.masked_array(data, [np.isnan(x) for x in data])
    print am

