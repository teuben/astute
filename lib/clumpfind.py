#! /usr/bin/env python
#
#  clumpfind wrapper (cf. the 3 in 1 Adam Leroy wrote)
#  cprops contains  (see also https://github.com/low-sky/cprops)
#
#    1) propdecomp (RL2006)
#    2) eclump (RB2005)
#    3) clfind (WdGB1994)
#
#  dendro comes from dendro-core
#    https://github.com/low-sky/dendro-core
#  but also note the IDL code in
#    https://github.com/low-sky/dendro


import sys
import runidl
import runsh
from astrodendro import Dendrogram
import pyfits


class ClumpFind(object):
    """
    Valid names are
    mir::clfind
    idl::clfind (or gdl)
    idl::cprops (or gdl)
    """
    def __init__(self,name='mir::clfind'):
        self.name = name
        self.valid = []
        self.register('mir::clfind')
        self.register('idl::clfind')
        self.register('idl::cprops')
    def myname(self):
        return self.name
    def register(self,name):
        self.valid.append(name)
    def runtest1(self,find=True,stats=True):
        x = runidl.IDL()
        if find:
            cmd=[]
            cmd.append(".run clfind")
            cmd.append("clfind,file='../data/ros13co',low=0.5,inc=0.5,/log")
            x.run(cmd)
        if stats:
            cmd=[]
            cmd.append(".run clstats")
            cmd.append("clstats,file='../data/ros13co',/log")
            x.run(cmd)
        # should see 105 clumps
    def runtest2(self,find=True,stats=True):
        print "You might need: fits in=ros13co.fits out=ros13co.mir op=xyin"
        print "Also note old .cf file not cleaned up"
        fin='in=../data/ros13co.mir'
        x = runsh.shell()
        if find:
            cmd=['clfind',fin,'dt=0.5','start=1','nmin=4']
            x.run(cmd)
        if stats:
            cmd=['clstats',fin,'dist=-1','xy=abs']
            x.run(cmd)
        # should see 95 clumps
    def runtest3(self):
        # dendro
        array = pyfits.getdata('../data/ros13co.fits')
        d = Dendrogram.compute(array,min_intensity=0.5,min_npix=8,min_delta=0.0)
        print "# DENDRO: Found %d clumps (leaves)" % len(d.leaves)
        n = 0
        nc = 0
        for l in d.leaves:
            nc = nc + 1
            n = n + len(l.f)
            (mom0,mom1,mom2)=imom(l.f,l.coords)
            print "%d   %f   %f %f %f    %f %f %f" % (nc, mom0, mom1[0],mom1[1], mom1[2], mom2[0],mom2[1],mom2[2])
        # immask: 60934 out of 100467 pixels are masked as good; 39533 were bad ( 39.35%)
        print "# DENDRO: Found %d assigned pixels in %d leaves" % (n,len(d.leaves))


        
def imom(f, xyz):
    n = len(f)
    m0 = 0
    mx1 = 0
    mx2 = 0
    my1 = 0
    my2 = 0
    mz1 = 0
    mz2 = 0
    for i in range(n):
        m0  = m0  + f[i]
        mx1 = mx1 + f[i]*xyz[i][0]
        my1 = my1 + f[i]*xyz[i][1]
        mz1 = mz1 + f[i]*xyz[i][2]
        mx2 = mx2 + f[i]*xyz[i][0]*xyz[i][0]
        my2 = my2 + f[i]*xyz[i][1]*xyz[i][1]
        mz2 = mz2 + f[i]*xyz[i][2]*xyz[i][2]
    mx1 = mx1/m0
    my1 = my1/m0
    mz1 = mz1/m0
    mx2 = mx2/m0 - mx1*mx1
    my2 = my2/m0 - my1*my1
    mz2 = mz2/m0 - mz1*mz1
    return ( m0, [mx1,my1,mz1], [mx2,my2,mz2] )
    


if __name__ == "__main__":
    # testing
    cf = ClumpFind()
    if sys.argv[1] == 'idl':
        cf.runtest1()
    if sys.argv[1] == 'mir':
        cf.runtest2()
    if sys.argv[1] == 'den':
        cf.runtest3()


