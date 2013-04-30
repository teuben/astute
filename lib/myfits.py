#

import pyfits

def doppler(file):
    h = pyfits.getheader(file)
    # d = pyfits.getdata(file)
    n3 = h.get('NAXIS3')
    f0 = h.get('CRVAL3')
    df = h.get('CDELT3')
    rf = h.get('RESTFRQ')
    c_kms = 299792.458
    dv = df/rf*c_kms

    print n3,f0,df,rf,dv
    
