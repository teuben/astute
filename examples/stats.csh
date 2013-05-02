#! /bin/csh -f
#
#  example spectral statistics for a fits cube, on which we can base
#  things like line identification, moment map generation etc.
#

set in=lsb

foreach _arg ($*)
  set $_arg
end


if (0) then
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
if (! -e $in) exit 1

set s=$in.stats


#  1) get a table with some stats per channel (this is the one that takes time)
ccdstat $in bad=0 robust=t planes=0 > $s.tab

#  2) plot of log(peak,rms,robust_rms) vs. channel
tabmath $s.tab - "$xvar,log(%4),log(%7),log(%14)" all |\
 tabplot - 1 2,3,4 line=1,1 xmin=$xl[1] xmax=$xl[2] ymin=-4 ymax=0 color=4,2,3 headline=$s \
    yapp=${s}_2a.ps/vcps


#  3a) plot of rms,robust_rms vs. channel, linear and in color, in mJy
tabmath $s.tab - "$xvar,%7,%14" all |\
 tabplot - 1 2,3 $xl[1] $xl[2] line=1,1 color=2,3 ymin=0 ymax=10 yscale=1000 headline=$s \
    yapp=${s}_3a.ps/vcps

#  3b) plot of Peak/Rms ("S/N")
tabmath $s.tab - $xvar,%4/%14 all |\
 tabplot - 1 2 $xl[1] $xl[2] 0 16 line=1,1 headline=$s yapp=${s}_3b.ps/vps


#  4a) histogram of robust values, outliers removed
tabhist $s.tab 14 .5 1.5 bins=32 nsigma=3 scale=1000 headline=$s yapp=${s}_4a.ps/vps

#  4b) histogram of the trended values
tabmath $s.tab - '%14*1000/sqrt(2)' all |\
 tabtrend - | tabhist - 1 -0.1 0.1 nsigma=3 headline=$s yapp=${s}_4b.ps/vps

