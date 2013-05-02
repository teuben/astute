#! /usr/bin/env python
#


# ccdmath  out=- fie='%x+10*%y+100*%z' size=4,3,2 cdelt=-0.01,0.01,1000 |\
# ccdfits - cube432.fits radecvel=true
# importfits('cube432.fits','cube432.im',overwrite=True)

import numpy as np

def test1(image):
    """
    fft the first plane
    """
    tb.open(image,nomodify=false);
    data=tb.getcol('map');
    shp=data.shape;
    td=data[0:shp[0],0:shp[1],0,0];
    ftd=np.fft.fft2(td);
    sftd=np.fft.fftshift(ftd);
    data[0:shp[0],0:shp[1],0,0]=sftd;
    tb.putcol('map',data);
    tb.close();

def test2(image):
    tb.open(image,nomodify=false);
    data = tb.getcol('map');
    shp = data.shape;
    for z in range(shp[2]):
        td = data[0:shp[0],0:shp[1],z,0];
        ftd=np.fft.fft2(td);
        sftd=np.fft.fftshift(ftd);
        data[0:shp[0],0:shp[1],z,0]=sftd;
    tb.putcol('map',data);
    tb.close();
