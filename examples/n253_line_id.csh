#! /bin/csh -f
#
#     use PV (or XYZ) correlation in a selected template to
#     find weaker lines
#

set in=pv1
set auto=1
#  the next 3 won't be used if auto=1
set v0=0
set v1=30
set ref=100.07640
#
set clip=0.01
set clip2=0.01
set vlsr=236
set yapp=/xs
set cmax=0.2
set rms=-1
set mode=1
set blines=$ASTUTE/etc/n253_lines.list
set fitsin=0

#  ieck, something one might want to pick the 2nd strongest line, not the first?
#  for example,set this to 2 if you want to the 2nd strongest line to match the
#  one detected in the peak of the PV/XYV map/cube
set line=1

# poor man's command line parser
foreach arg ($*)
  set $arg
end


# ---- below this nothing ought to be changed ----

set c=299792.458

set dir=`pwd`
set cdir=$dir:t

if ($auto) then
  set v01=()
  set ref=0
else
  set v01=(v0=$v0 v1=$v1)
endif

if ($fitsin) then
  rm pv1
  fitsccd in=PV.fits out=pv1 
endif

echo =========================================================================
echo Bootstrap Line Identification in `pwd`
tabmath ccdstat.tab - %2/1e9,%4/%14 all > line_bs.tab
tabpeak line_bs.tab mean=t clip=10 | sort -k 3 -nr  > line_bss.tab
if (-z line_bss.tab) then
  echo BAD NEWS: no strong lines to bootstrap from? decrease clip=10?
endif
set f=(`head -1 line_bss.tab | awk '{print $1}'`)
set f0=`nemoinp "$f/(1-$vlsr/$c)" format=%f`
grep -v ^\# $blines | awk 'function abs(x) {return ((x<0.0)?-x:x)}{print abs($1-'$f0'),$1,$2}' | sort -n > lines_bsd.tab
echo -n "LINE_ID: "
head -$line lines_bsd.tab | tail -1
if ($ref == 0 || $auto == 1) then
  set ref=`head -$line lines_bsd.tab | tail -1  | awk '{print $2}'`
  echo Using ref=$ref
endif
echo =========================================================================


echo "STATS on $in (robust)"
ccdstat $in robust=t bad=0
rm -f $in.template
echo PVCORR clip=$clip mode=$mode
echo pvcorr  $in     clip=$clip $v01 vscale=1e-9 rms=$rms mode=$mode out=$in.template 
pvcorr  $in     clip=$clip $v01 vscale=1e-9 rms=$rms mode=$mode out=$in.template > $in.tab
tabpeak $in.tab clip=$clip2 > $in.peak
# take both the peaks and valleys and from the robust sigma maybe get an idea
# what a good value for $clip2 should be
echo =========================================================================
echo TABHIST: tabpeak $in.tab - check what clip2 might be better to cut out peaks from the noise
echo suggestion: Take the smallest of -datamin and robust sigma
tabpeak $in.tab valley=t | tabhist - 2 robust=t yapp=/null
echo =========================================================================

set ref0=`sort -k 2 -nr $in.peak | head -1 | awk '{print $1}'`
set ref1=`nemoinp "(1-$vlsr/$c)*$ref" format=%f`
echo REF0=$ref0  REF1=$ref1 REF=$ref
echo "# SkyFreq   RestFreq    Corr"
tabmath $in.peak - "%1-($ref0)+$ref1,%3/(1-$vlsr/$c),%2" all format=%f 
tabmath $in.tab  - "%1-($ref0)+$ref1,%4/(1-$vlsr/$c),%2" all format=%f > $in.tab2
tabplot $in.tab2 2 3 ymin=-$cmax ymax=$cmax point=2,0.1 line=1,1 color=2 ycoord=0,$clip2 headline=$cdir xlab=RestFreq yapp=$yapp

if (0) then
  # the wrong way, doppler shifts are tricky, especially if the band is going to be wide and/or low freq
  tabmath $in.tab  - "%1-($ref0)+$ref,%4/(1-$vlsr/$c),%2" all format=%f > $in.tab3
  tabplot $in.tab3 1 3 100 102 ymin=-0.2 ymax=0.2 point=2,0.1 line=1,1 color=2 ycoord=0,0.01 headline=$cdir yapp=$yapp
endif

if (-e mlines.list) then
   echo MLINES.LIST:
   cat mlines.list
endif
