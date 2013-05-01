#! /bin/csh -f
#
#  example spectral statistics for a fits cube, on which we can base
#  things like line identification, moment map generation
#  benchmark:  4'53" on NEMO2  (7'50" before the ini_moment bug)
#             10'02" on DANTE  (single) - go figure!
#              4'59" on DANTA  (double)

set lsb=ngc253_fullcube_compact_LSB_contsub_clean.fits
set usb=ngc253_fullcube_compact_USB_contsub_clean.fits 

#  0) sanity check on file existence
if (! -e $lsb) exit 1
if (! -e $usb) exit 1

#  1) get a table with some stats per channel
fitsccd $lsb - | ccdstat - bad=0 robust=t planes=0 >  LSB.tab

fitsccd $usb - | ccdstat - bad=0 robust=t planes=0 > USB.tab

#  2) plot of log(peak,rms,robust_rms) vs. channel

tabmath LSB.tab - '%1,log(%3),log(%6),log(%13)' all |\
 tabplot - 1 2,3,4 line=1,1 xmin=0 xmax=600 ymin=-4 ymax=0 color=4,2,3 yapp=LSB_2a.ps/vcps

tabmath USB.tab - '%1,log(%3),log(%6),log(%13)' all |\
 tabplot - 1 2,3,4 line=1,1 xmin=0 xmax=600 ymin=-4 ymax=0 color=4,2,3 yapp=USB_2a.ps/vcps

#  3a) plot of rms,robust_rms vs. channel, linear and in color, in mJy
tabplot LSB.tab 1 6,13 0 600 line=1,1 color=2,3 ymin=0 ymax=10 yscale=1000 yapp=LSB_3a.ps/vcps
tabplot USB.tab 1 6,13 0 600 line=1,1 color=2,3 ymin=0 ymax=10 yscale=1000 yapp=USB_3a.ps/vcps


#  3b) plot of Peak/Rms ("S/N")
tabmath LSB.tab - %1,%3/%13 all | tabplot - 1 2 0 600 0 16 line=1,1 yapp=LSB_3b.ps/vps
tabmath USB.tab - %1,%3/%13 all | tabplot - 1 2 0 600 0 16 line=1,1 yapp=USB_3b.ps/vps


#  4a) histogram of robust values, outliers removed
tabhist LSB.tab 13 .5 1.5 bins=32 nsigma=3 scale=1000 yapp=LSB_4a.ps/vps
#  -> Mean and dispersion  : 1.0814 0.0444432 (dispersion/trend = 1.5 = modest)
tabhist USB.tab 13 0  4   bins=32 nsigma=3 scale=1000 yapp=USB_4a.ps/vps
#  -> Mean and dispersion  : 2.03947 0.265749  (dispersion/trend = 3.8 = strong)


#  4b) histogram of the trended values
tabmath LSB.tab - '%13*1000/sqrt(2)' all | tabtrend - | tabhist - 1 -0.1 0.1 nsigma=3 yapp=LSB_4b.ps/vps
#  -> Mean and dispersion  : 1.80987e-05 0.0295542 
tabmath USB.tab - '%13*1000/sqrt(2)' all | tabtrend - | tabhist - 1 -0.3 0.3 nsigma=3 yapp=USB_4b.ps/vps
#  -> Mean and dispersion  : 0.00203996 0.0703949

