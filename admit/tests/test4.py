#
#   testing creating  (with and without the abc math)
#   1000     0.164u  0.104s 0:00.29 89.6%	0+0k 32+8000io 0pf+0w
#            0.176u  0.088s 0:00.27 92.5%	0+0k 0+8000io 0pf+0w
#   10000    0.388u  0.604s 0:01.75 56.0%	0+0k 2952+80000io 13pf+0w
#            0.764u  0.928s 0:02.11 79.6%	0+0k 0+80000io 0pf+0w
#            0.584u  0.806s 0:02.29 60.2%       0+0k 800+80088io 1pf+0w  [dante]
#   100000   3.336u  6.124s 0:38.99 24.2%	0+0k 2216+800000io 1pf+0w
#            4.068u  5.892s 0:36.98 26.9%	0+0k 0+800000io 0pf+0w
#            3.996u 10.771s 0:50.55 29.1%       0+0k 6336+800096io 1pf+0w [dante]
#   -> about 0.2 - 0.5 ms per directory visit.
#      csh is about 10-20 slower in wall clock time,         

import os, sys
import admit.adm     as admit
import admit.parfile as parfile



if __name__ == '__main__':
    print "ADMIT::test4"
    a=admit.ADMIT(debug=False)
    d=a.query_dir()
    n = 10
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    do_par = True
    do_add = True
    print "Preparing %d directories under manydata/" % n
    for i in range(n):
        id = '%06d' % i
        a.setdir('manydata/%s' % id)
        if do_par:
            p = parfile.ParFile()
            p.set('project',id)
            if do_add:
                p.set('a','3')
                p.set('b','4')
                a1 = p.geti('a')
                b1 = p.geti('b')
                c1 = a1+b1
                p.set('c','%d' % c1)
            p.save()
        a.tesdir()
    #
