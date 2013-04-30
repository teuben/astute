import pyfits,sys
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt

d = pyfits.getdata(sys.argv[1])[0]
d = np.nan_to_num(d)

thres = 0.005
#setup a mask
mask = d > thres

#segment the image
label_im, nb_labels = ndimage.label(mask)

minvoxels = 30

#drop small segments
rem = []
for i in range(1,nb_labels+1):
    if (np.count_nonzero(label_im==i) < minvoxels):
        label_im[label_im==i] = 0
    else:
        rem += [i]
print rem

label_im.astype(np.uint8).tofile(sys.argv[2])

#process each component
f, axarr = plt.subplots(len(rem), sharex=True)
for i,r in enumerate(rem):
    itemidx = np.where(label_im ==r)
    iteminten = d[itemidx]
    
    witemidx = itemidx* iteminten
    
    #center of mass
    wcom = np.mean(witemidx,axis=1)
    com = wcom/np.mean(iteminten)

    #compute the cov and svd
    nitem = (witemidx-wcom[:,np.newaxis])
    cov = np.dot(nitem,nitem.T)
    u,s,v = np.linalg.svd(cov)
    print v


    hist, bound = np.histogram(iteminten,bins=256,
                               range=(thres,np.max(d)))
    axarr[i].hist(iteminten,bins=256,range=(thres,np.max(d)))

plt.show()
