#! /bin/csh -f
#
# overlap integral example

set all=(w_0_c/L_co w_1_c/L_c17o w_1_c/L_cn_1 w_1_c/L_cn_2 w_2_c/L_hc3n w_2_c/L_ch3oh w_2_c/L_h2cs_1 w_3_c/L_ch3c2h)

set mol=(co c17o cn_1 cn_2 hc3n ch3oh h2cs_1 ch3c2h)


set n=1
foreach m ($mol)
  echo $m $n
  @ n*=2
end
exit 0

set n=0


foreach a ($all)
   @ n++
   set fits=$a/MOM0.fits
   fitsccd in=$fits out=$a/nemo error=1
   if ($n == 1) then
     set mask=$a/nemo
   else
     set mask=$mask,$a/nemo
   endif
end

echo mask=$mask
