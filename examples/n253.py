#
# casapy script, with some external MIRIAD and NEMO example calls
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
import astute, alines
import sys

tin   = 'ngc253_fullcube_%s_SPW_%d_contsub_clean'     # the long name
tout  = 'w_%d_%s'                                     # i'm lazy, make a short name
conf  = ['extended','compact']                        # two configurations
#conf  = ['compact']                        # two configurations
spw   = [0,1,2,3]                                     # 4 spectral windows
cfits = False                                         # produce center fits files
Qline = True                                          # only do line ID stuff, no NEMO and MIRIAD cubestats
Qone  = False                                         # only do first spw

Qline = True


# 
vlsr  = 236.0                               # VLSR needed
pvseg = { "e" : [[262,359],[385,277]] , "c" :  [[239,369],[419,260]] }       # PV segments in extended/compact
vcube = [-50,550]                           # V around the VLSR in which individual spectral line cubes are cut

a = astute.Astute()
#a.need(['NEMO','MIRIAD'])                             # this script needs NEMO & MIRIAD

#  cheat , or use slsearch() later on, or try datasplat
(freq,line) = alines.read_cheat_lines('n253_lines.list')


for c in conf:             # loop over configurations and spectral_windows
    for s in spw:
        iname = tin % (c,s)
        oname = tout % (s,c[0])
        
        # Q?  should mkdir 'oname' and put IM in oname/IM ?
        # need a generic way to grab a FITS file and build our own XML container
        f_fits = iname + ".fits"
        f_im   = oname + "/im"
        f_pv   = oname + '/PV'
        print " ====== Working on ",f_fits," converting into ",oname," ======"
        # os.system("rm -rf %s; mkdir %s" % (oname,oname))
        importfits(f_fits, f_im, overwrite=True)
        h = imhead(f_im,mode='list')
        naxis = h['shape']
        naxis3 = naxis[2]
        crval3 = h['crval3']/1e9
        cdelt3 = h['cdelt3']/1e9
        crpix3 = h['crpix3'] + 1     #  note CASA does 0 based here
        # imstat axes=[0,1]
        #
        #
        [freq0,freq1] = alines.axis_range(naxis3, crval3, cdelt3, crpix3)
        freq0_0 = alines.f_rest(vlsr,freq0)
        freq1_0 = alines.f_rest(vlsr,freq1)
        print "Range in sky  freq:",freq0,freq1
        print "Range in rest freq:",freq0_0,freq1_0," for vlsr=",vlsr
        slsearch(logfile=oname+"/slines.list",verbose=True,freqrange=[freq0_0,freq1_0])
        alines.edit_slines_doppler(oname+"/slines.list",vlsr)
        fp = open(oname+"/mlines.list","w")
        nlines = 0
        for i in range(len(freq)):
            # see if doppler shifted line in this spw
            f = alines.f_doppler(vlsr,freq[i])
            if alines.in_range(f, naxis3, crval3, cdelt3, crpix3):
                nlines = nlines + 1
                fp.write("%f %s\n" % (freq[i],line[i]))
                l_out = oname+"/L_"+line[i]
                imsubimage(f_im,l_out,overwrite=True,chans="range=[%gkm/s,%gkm/s], restfreq=%gGHz" % (vcube[0],vcube[1],freq[i]))
                imreframe(l_out,restfreq='%gGHz' % freq[i])
                # figure out the RMS at this freq by interpolating from a smooth RMS(freq) graph
                # from cubestats
                # then use excludepix=[-2,2]
                immoments(l_out,outfile=l_out+"/MOM0")
                h0 = imstat(l_out+"/MOM0")
                print "in_range: ",f,"(",line[i],"@",freq[i],")"," Peak/Flux/RMS=",h0['max'],h0['flux'],h0['rms']
                exportfits(l_out+"/MOM0",l_out+"/MOM0.fits",velocity=True)
        print "Identified %d lines (still faking it)" % nlines
        fp.close()
        impv(f_im,f_pv,pvseg[c[0]][0],pvseg[c[0]][1],overwrite=True)
        exportfits(f_pv,f_pv+'.fits',overwrite=True)
                
        if cfits:
            imsubimage(oname,oname+'/c',region='box[[274pix,276pix], [373pix,350pix]]')
            exportfits(oname+'/c',oname+'/center.fits')
        if Qone: break
        if Qline:
            continue
        if a.has('NEMO'):
            a.nemo('fitsccd in=%s.fits out=%s/nemo' % (iname,oname))
            a.nemo('ccdstat %s/nemo bad=0 robust=t planes=0 > %s/ccdstat.tab' % (oname,oname))
        if a.has('MIRIAD'):
            a.miriad('fits in=%s.fits out=%s/mir op=xyin' % (iname,oname))
            a.miriad('velsw in=%s/mir axis=radio' % (oname))
            a.miriad('imstat in=%s/mir log=%s/imstat.tab' % (oname,oname))
    if Qone: break
