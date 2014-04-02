#
#   testing creating 
#   1000     0.164u 0.104s 0:00.29 89.6%	0+0k 32+8000io 0pf+0w
#   10000    0.388u 0.604s 0:01.75 56.0%	0+0k 2952+80000io 13pf+0w
#   100000   3.336u 6.124s 0:38.99 24.2%	0+0k 2216+800000io 1pf+0w


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
    print "Preparing %d directories" % n
    for i in range(n):
        id = '%06d' % i
        a.setdir('manydata/%s' % id)
        p = parfile.ParFile()
        p.set('project',id)
        p.save()
        a.tesdir()
    #
