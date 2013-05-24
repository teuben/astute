#
# casa script, with some MIRIAD and NEMO example calls
# To run this:
#     casapy --nogui -c $ASTUTE/examples/n253.py
#
# it would be useful to find out if there is some "import casa" style,
# so you don't have to run this from within casapy?
#
# To grab the original data, get the extended and compact cubes from
# http://www.astro.umd.edu/~bolatto/NGC253/cubes/compact/newrelease/lines/individual_spws/
# http://www.astro.umd.edu/~bolatto/NGC253/cubes/extended/newrelease/lines/individual_spws/
#
# the big steps are ccdstat, these 8 cubes takes:   383.777u 49.244s 7:35.90 94.9% 
# just importfits                                    12.114u  5.752s 0:29.33 60.8%    
# with imhead                                        21.526u  7.193s 0:44.55 64.4%   
# with nemo fitsccd                                  39.267u 12.747s 1:15.89 68.5%   
# all                                               416.134u 16.151s 7:27.07 96.6% 

#  central box to pick 274,276, 373,350

#   from astute
import astute

tin  = 'ngc253_fullcube_%s_SPW_%d_contsub_clean'      # the long name
tout = 'w_%d_%s'                                      # i'm lazy, make a short name
conf  = ['extended','compact']                        # two configurations
spw   = [0,1,2,3]                                     # 4 spectral windows

a = astute.Astute()
a.need(['NEMO','MIRIAD'])                             # this script needs NEMO & MIRIAD

for c in conf:             # loop over configurations and spectral_windows
    for s in spw:
        iname = tin % (c,s)
        oname = tout % (s,c[0])
        
        # Q?  should mkdir 'oname' and put IM in oname/IM ?
        print " ====== Working on ",iname," converting to ",oname," ======"
        importfits(iname + ".fits", oname, overwrite=True)
        h = imhead(oname,mode='list')
        naxis = h['shape']
        naxis3 = naxis[2]
        print naxis3
        if a.has('NEMO'):
            a.nemo('fitsccd in=%s.fits out=%s/nemo' % (iname,oname))
            a.nemo('ccdstat %s/nemo bad=0 robust=t planes=0 > %s/ccdstat.tab' % (oname,oname))
        if a.has('MIRIAD'):
            a.miriad('fits in=%s.fits out=%s/mir op=xyin' % (iname,oname))
            a.miriad('velsw in=%s/mir axis=radio' % (oname))
            a.miriad('imstat in=%s/mir log=%s/imstat.tab' % (oname,oname))
