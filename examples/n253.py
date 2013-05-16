#
# casa script, with some MIRIAD and NEMO example calls
#
# needed at the extended and compact cubes from
# http://www.astro.umd.edu/~bolatto/NGC253/cubes/compact/newrelease/lines/individual_spws/
# http://www.astro.umd.edu/~bolatto/NGC253/cubes/extended/newrelease/lines/individual_spws/


#   from astute
import myfits
import astute
import runsh

template = 'ngc253_fullcube_%s_SPW_%d_contsub_clean'
conf  = ['extended','compact']
spw   = range(4)

a = astute.Astute()
a.need(['NEMO','MIRIAD'])

for c in conf:
    for s in spw:
        name = template % (c,s)
        importfits(name + ".fits", name, overwrite=True)
        if a.has('NEMO'):
            cmd = 'fitsccd in=%s.fits out=%s/nemo' % (name,name)
            a.shell(cmd.split())
            # a.nemo(cmd)
        if a.has('MIRIAD'):
            cmd = 'fits in=%s.fits out=%s/mir op=xyin' % (name,name)
            a.shell(cmd.split())
            # a.miriad(cmd)
            
