#
#   source this in casapy
#
f = ['bench512.fits', 'b1.n2hp.peter.fits', 'orionall_hannclean_hotcore_cube.fits']
f = ['bench-cube.fits', 'bench-slab.fits', 'bench-stick.fits']
d = ['CUBE',            'SLAB',            'STICK']

#  cut and paste from below

import os



# set this
test = 0      # pick 0,1,2

# cut and paste from here down

fits_file = f[test]
run_dir   = d[test]

print 'TEST: ',fits_file,run_dir

cmd = 'rm -rf %s/c.*' % run_dir
print 'CMD: ',cmd
os.system(cmd)

im1 = run_dir + '/' + 'c.1'
print 'IM1=',im1
h = [im1+'.h0',  im1+'.h1',  im1+'.h2']

# the benchmark starts

%time importfits(fits_file, im1)
%time ia.open(im1)
%time ia.statistics()
for i in [0,1,2]:
  %time ia.hanning(outfile=h[i],axis=i,drop=False,overwrite=True)
# seems a bug, the overwrite doesn't work

%time immath(imagename=[im1,im1],expr='IM0+IM1',outfile=im1+'.a')

# 
%time importfits(fits_file, im1)
%time ia.open(im1)
%time ia.statistics()
%time ia.hanning(outfile=h[0],axis=0,drop=False,overwrite=True)
%time ia.hanning(outfile=h[1],axis=1,drop=False,overwrite=True)
%time ia.hanning(outfile=h[2],axis=2,drop=False,overwrite=True)
# seems a bug, the overwrite doesn't work
%time immath(imagename=[im1,im1],expr='IM0+IM1',outfile=im1+'.a')

def runme(fits_file, im1):
  importfits(fits_file, im1)
  ia.open(im1)
  ia.statistics()
  for i in [0,1,2]:
    ia.hanning(outfile=h[i],axis=i,drop=False,overwrite=True)
  immath(imagename=[im1,im1],expr='IM0+IM1',outfile=im1+'.a')
  ia.close()

%time runme(fits_file,im1)

