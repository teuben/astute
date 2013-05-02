#! /bin/csh -f
#
#  example spectral statistics for a fits cube, on which we can base
#  things like line identification, moment map generation etc.
#  benchmark:  4'53" on NEMO2  (7'50" before the ini_moment bug)
#             10'02" on DANTE  (single) - go figure!
#              4'59" on DANTA  (double)

set lsb=ngc253_fullcube_compact_LSB_contsub_clean.fits
set usb=ngc253_fullcube_compact_USB_contsub_clean.fits 


if (1) then
  # freq in GHz
  set xvar=%2/1e9
  set xl=(99.5 103.5)
  set xu=(112 116)
else
  # channel number
  set xvar=%1
  set xl=(0 600)
  set xu=(0 600)
endif

#  0) sanity check on file existence
if (! -e $lsb) exit 1
if (! -e $usb) exit 1


#  1) get a table with some stats per channel
fitsccd $lsb - | ccdstat - bad=0 robust=t planes=0 > LSB.tab
fitsccd $usb - | ccdstat - bad=0 robust=t planes=0 > USB.tab


#  2) plot of log(peak,rms,robust_rms) vs. channel
tabmath LSB.tab - "$xvar,log(%4),log(%7),log(%14)" all |\
 tabplot - 1 2,3,4 line=1,1 xmin=$xl[1] xmax=$xl[2] ymin=-4 ymax=0 color=4,2,3 yapp=LSB_2a.ps/vcps
tabmath USB.tab - "$xvar,log(%4),log(%7),log(%14)" all |\
 tabplot - 1 2,3,4 line=1,1 xmin=$xu[1] xmax=$xu[2] ymin=-4 ymax=0 color=4,2,3 yapp=USB_2a.ps/vcps


#  3a) plot of rms,robust_rms vs. channel, linear and in color, in mJy
tabmath LSB.tab - "$xvar,%7,%14" all |\
 tabplot - 1 2,3 $xl[1] $xl[2] line=1,1 color=2,3 ymin=0 ymax=10 yscale=1000 yapp=LSB_3a.ps/vcps
tabmath USB.tab - "$xvar,%7,%14" all |\
 tabplot - 1 2,3 $xu[1] $xu[2] line=1,1 color=2,3 ymin=0 ymax=10 yscale=1000 yapp=USB_3a.ps/vcps

#  3b) plot of Peak/Rms ("S/N")
tabmath LSB.tab - $xvar,%4/%14 all |\
 tabplot - 1 2 $xl[1] $xl[2] 0 16 line=1,1 yapp=LSB_3b.ps/vps
tabmath USB.tab - $xvar,%4/%14 all |\
 tabplot - 1 2 $xu[1] $xu[2] 0 16 line=1,1 yapp=USB_3b.ps/vps


#  4a) histogram of robust values, outliers removed
tabhist LSB.tab 14 .5 1.5 bins=32 nsigma=3 scale=1000 yapp=LSB_4a.ps/vps
#  -> Mean and dispersion  : 1.0814 0.0444432 (dispersion/trend = 1.5 = modest)
tabhist USB.tab 14 0  4   bins=32 nsigma=3 scale=1000 yapp=USB_4a.ps/vps
#  -> Mean and dispersion  : 2.03947 0.265749  (dispersion/trend = 3.8 = strong)

#  4b) histogram of the trended values
tabmath LSB.tab - '%14*1000/sqrt(2)' all |\
 tabtrend - | tabhist - 1 -0.1 0.1 nsigma=3 yapp=LSB_4b.ps/vps
#  -> Mean and dispersion  : 1.80987e-05 0.0295542 
tabmath USB.tab - '%14*1000/sqrt(2)' all |\
 tabtrend - | tabhist - 1 -0.3 0.3 nsigma=3 yapp=USB_4b.ps/vps
#  -> Mean and dispersion  : 0.00203996 0.0703949

