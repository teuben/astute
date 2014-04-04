#! /bin/csh -f
#
#    create N directories, and write a small file in it, see test4.py
#
#  1000   :  0.164u  0.264s 0:03.77 11.1%	0+0k 144+8000io 0pf+0w
#  10000  :  1.136u  2.840s 0:34.43 11.5%	0+0k 3232+80000io 0pf+0w
#  100000 : 11.944u 36.008s 6:26.72 12.3%	0+0k 13576+800048io 11pf+0w

set n=1000


foreach arg ($*)
  set $arg
end

echo n=$n

foreach i (`seq $n`)
    set ip=`printf %06d $i`
    # echo $ip
    set dip=manydata/$ip
    mkdir -p $dip
    echo project=$ip > $dip/tas.def
end
