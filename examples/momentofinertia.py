#! /usr/bin/env python
#
#
#   shape analysis tool, based on moments of inertia in the clumps
#   June 2013 : Original version   -   Cheuk Yiu Ip
#
#
#   Warning:   clfind uses 0 for no clump, >=1 for clumpid
#              dendro uses 0...N for clumpid,  32767 for no clump 
#   Watch out for 4D cubes...

import pyfits,sys
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import sklearn.decomposition
import sklearn.manifold

#argv[1] is fits file, argv[2] is a fits file with clumps ID
d = pyfits.getdata(sys.argv[1])
d = np.nan_to_num(d)
dm = pyfits.getdata(sys.argv[2])
dm = np.nan_to_num(dm)

ntot = d.shape[0] * d.shape[1] * d.shape[2]
if d.shape[0] == 1:
    print d.shape
    print dm.shape
    sys.exit(0)

if len(sys.argv) == 4:
    """
    this ascii output makes it easy to convert to a snapshot in NEMO
    and use its tools to do a shape analysis (e.g. snaprect/snapkinem/)
    Example:
    ./momentofinteria.py data.fits mask.fits 10 | grep -v ^# | tabtos - clump10.ss nbody mass,pos
    """
    clump_id = int(sys.argv[3])
    itemidx = np.where(dm==clump_id)
    iteminten = d[itemidx]
    coord = np.vstack(itemidx).astype(np.float32)
    n = len(itemidx[0])
    print "# File: %s Clump: %d" % (sys.argv[1],clump_id)
    print "# Flux, X, Y, Z/VZ"
    print n
    for i in range(n):
        print iteminten[i],coord[2][i],coord[1][i],coord[0][i]
    sys.exit(0)
    


# serpens needs [0:-1], ros13 needs [1:]
# serpens also need to rid the 4th dimension
rem = np.unique(dm)[1:]
#rem = np.unique(dm)[0:-1]

#process each component
#f, axarr = plt.subplots(len(rem), sharex=True)
#[gx,gy,gz] = np.gradient(d)

ncl = len(rem)
desc = np.zeros((ncl,5))

nic = 0
for i,r in enumerate(rem):
    print "=============: ",i
    itemidx = np.where(dm==r)
    iteminten = d[itemidx]
    coord = np.vstack(itemidx).astype(np.float32)
    nic = nic + coord.shape[1]
    print coord.shape,coord
    coord -= np.mean(coord,axis=1)[:,np.newaxis]
    print coord
    intencoord = coord*iteminten
    covar =  np.dot(intencoord,intencoord.transpose())
    print '3D:',covar
    print '2D:',covar[0:2,0:2]
    u1,s1,v1=np.linalg.svd(covar[0:2,0:2])
    u2,s2,v2=np.linalg.svd(covar)
    print u1,s1,v1,'|',u2,s2,v2
    desc[i,:] = np.hstack((s1,s2))

print "==================: ",desc.shape
print "Note: ",nic,"/",ntot," pixels in ",ncl," assigned clumps"

#PCA
Y = sklearn.decomposition.PCA(n_components=2).fit_transform(desc)
plt.figure("pca")
plt.scatter(Y[:,0], Y[:,1],linewidth=0)
plt.savefig("pca.png")

#MDS
Y = sklearn.manifold.SpectralEmbedding(n_components=2).fit_transform(desc)
plt.figure("Spectral")
plt.scatter(Y[:,0], Y[:,1],linewidth=0)
plt.savefig("spectral.png")
plt.show()




    #(gx[itemidx]*d[itemidx],
    # gy[itemidx]*d[itemidx],
    # gz[itemidx]*d[itemidx])
    

    
#     witemidx = itemidx* iteminten
    
#     #center of mass
#     wcom = np.mean(witemidx,axis=1)
#     com = wcom/np.mean(iteminten)

#     #compute the cov and svd
#     nitem = (witemidx-wcom[:,np.newaxis])
#     cov = np.dot(nitem,nitem.T)
#     u,s,v = np.linalg.svd(cov)
#     print v


#     hist, bound = np.histogram(iteminten,bins=256,
#                                range=(thres,np.max(d)))
#     axarr[i].hist(iteminten,bins=256,range=(thres,np.max(d)))

# plt.show()
