import pyfits,sys
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
import sklearn.decomposition
import sklearn.manifold

#argv[1] is fits file, argv[2] is a fits file with clumps ID
d = pyfits.getdata(sys.argv[1])
d = np.nan_to_num(d)
label_im = pyfits.getdata(sys.argv[2])

rem = np.unique(label_im)[1:]

#process each component
#f, axarr = plt.subplots(len(rem), sharex=True)
#[gx,gy,gz] = np.gradient(d)

desc = np.zeros((len(rem),5))

for i,r in enumerate(rem):
    itemidx = np.where(label_im ==r)
    iteminten = d[itemidx]
    coord = np.vstack(itemidx).astype(np.float32)
    coord -= np.mean(coord,axis=1)[:,np.newaxis]
    intencoord = coord*iteminten
    covar =  np.dot(intencoord,intencoord.transpose())
    u1,s1,v1=np.linalg.svd(covar[0:2,0:2])
    u2,s2,v2=np.linalg.svd(covar)
    desc[i,:] = np.hstack((s1,s2))

print desc.shape 

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
