#! /usr/bin/env python
#
# simple dependency/graph theory of BDP's
# this shows a way to build a dependency tree of BDP's
# 
# to note:
#    BDP's are always needed as input/output for an AT, they will
#    then be contained within an AT
#    
#  bench:
#    1 1000    0.04      1000   1   0.07"
#    1 10000   0.35"     10000  1   0.88
#    1 100000  4.5"      100000 1  10.4
#
#    100 100   0.35
#   1000 100   4.3
#    100 1000  4.6
#   1000 1000  45"    (6GB memory!)

import sys


_debug = False

nprojects = 100
nlines    = 100

class ADMIT(object):
    def __init__(self, name='none'):
        self.name    = name
        self.bdps    = []

class BDP(object):
    def __init__(self, name='none', filename='foobar'):
        self.name     = name
        self.filename = filename
        self.updated  = False
        self.deps     = []
        self.derv     = []
        self.task     = None
        if _debug: print "BDP(%s) " % name
    def show(self):
        return self.name
    def update(self,new_state):
        if _debug: print "UPDATE: %s" % self.name
        self.updated = new_state
        for d in self.derv:
            d.update(new_state)
    def depends_on(self,other):
        if other == None: return
        if _debug: print 'BDP %s depends on %s' % (self.name,other.show())
        self.deps.append(other)
        other.derv.append(self)
    def report(self):
        print "===report==="
        print "BDP::%s" % self.name
        for d in self.deps:
            print "BDP::deps %s" % d.show()
        for d in self.derv:
            print "BDP::derv %s" % d.show()
        print "BDP::task %s" % self.task.show()
    def set(self,keyval):
        if _debug: print "BDP::set %s" % keyval
    def run(self):
        if self.updated: 
            if _debug: print "BDP::%s (%s) was up to date" % (self.name,self.filename)
            return False
        if _debug: print "BDP::%s (%s) running" % (self.name,self.filename)
        if self.task == None:
            if _debug: print " Warning: no task set ???"
            # raise ?
        else:
            self.task.run()
        self.updated = True
        return True

def DependsOn(a,b):
    """ b depends on a """
    b.depends_on(a)

class AT(object):
    name    = 'generic'
    version = '1.0'
    keys    = ['alpha', 'beta', 'gamma']
    def __init__(self,name='none',bdp_in=[],bdp_out=[]):
        if _debug: print "AT.init(%s)" % name
        self.name    = name
        self.bdp_in  = bdp_in
        self.bdp_out = bdp_out
        for b2 in bdp_out:
            b2.task = self
            for b1 in bdp_in:
                b2.depends_on(b1)
    def show(self):
        return self.name
    def run(self):
        if _debug: print "AT.run(%s)" % self.name
        do_nothing = True
        for b2 in self.bdp_out:
            if not b2.updated: do_nothing = False
        if do_nothing:
            if _debug: print "   no work needed here"
            return False
        for b2 in self.bdp_out:
            b2.updated = True
        return True
    def set(self,keyval):
        for b2 in self.bdp_out:
            if b2.updated:
                b2.update(False)
    def rerun(self):
        if _debug: print "AT.rerun(%s)" % self.name
    def report(self):
        print "AT: ",self.name
        if len(self.bdp_in) > 0:
            print "  BDP_IN:"
            for b in self.bdp_in:  print "    ",b.show()
        if len(self.bdp_out) > 0:
            print "  BDP_OUT:"
            for b in self.bdp_out:  print "    ",b.show()


class AT_ingest(AT):
    name = 'INGEST'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_ingest.init"
    def run(self):
        if _debug: print "AT_ingest.run"
        if not AT.run(self):
            return False
        # specialized work can commence here



class AT_combine(AT):
    name = 'COMBINE'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        if _debug: print "AT_combine.init"
    def run(self):
        if _debug: print "AT_combine.run"
        if not AT.run(self):
            return False
        # specialized work can commence here
        print "  work: %d -> %d" % (len(self.bdp_in),len(self.bdp_out))
        print "  in:  ",self.bdp_in[0].show(),self.bdp_in[1].show()
        print "  out: ",self.bdp_out[0].show()



class AT_flow(AT):
    name = 'FLOW'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        if _debug: print "AT_flow.init"
        AT.__init__(self,self.name,bdp_in,bdp_out)
    # note the deliberate bug to not implement the .run() here




def pipeline(bdps):
    if _debug: print "===============   Running pipeline ============="
    for b in bdps:
        b.run()


def try1(do_show=True, do_dep=True):
    bdps = []
    b0 = BDP('foobar0.fits')          ; bdps.append(b0)
    b1 = BDP('foobar1.fits')          ; bdps.append(b1)
    a0 = AT_ingest([],[b0])      
    a1 = AT_ingest([],[b1])      
    a0.run()
    a1.run()



    b2 = BDP('foobar2.cim')           ; bdps.append(b2)
    a2 = AT_combine([b0,b1],[b2])
    a2.run() 

    b3 = BDP('foobar3.cim')           ; bdps.append(b3)
    a3 = AT_flow([b2],[b3])
    a3.run()

    if do_show:
        for b in bdps:
            print "b-SHOW: ",b.show()
        for a in [a0,a1,a2,a3]:
            print "a-SHOW: ",a.show()

    if do_dep:
        print "### these should now be up to date"
        for b in bdps:
            b.run()
        print "### a1.set()"
        a1.set('alpha=1.0')
        print "### these should now be creating new b2 and down"
        for b in bdps:
            b.run()

def try2(nlines=1):
    bdps = []
    b0 = BDP('foobar.fits')                 ; bdps.append(b0)
    b1 = BDP('foobar.cim')                 ; bdps.append(b1)
    a1 = AT('ingest',[b0],[b1])            
    a1.run()
  
    b2 = BDP('Summary','foobar.sum')       ; bdps.append(b2)
    a2 = AT('Summary',[b1],[b2])
    a2.run()

    b3 = BDP('CubeStats','foobar.cs')       ; bdps.append(b3)
    a3 = AT('CubeStats',[b1],[b3])
    a3.run()

    b4 = BDP('LineList','foobar.ll')       ; bdps.append(b4)
    a4 = AT('LineList',[b3],[b4])
    a4.run()


    #
    b5 = range(nlines)
    a5 = range(nlines)
    b6 = range(nlines)
    a6 = range(nlines)
    b7 = range(nlines)
    a7 = range(nlines)
    b8 = range(nlines)
    a8 = range(nlines)

    for l in range(nlines):

        basename = 'linecube.%05d' % (l+1)

        b5[l] = BDP('LineCube',basename+'.cim')       ; bdps.append(b5[l])
        a5[l] = AT('LineCube',[b1,b4],[b5[l]])
        a5[l].set('dv=100')
        a5[l].run()

        b6[l] = BDP('Mom0',basename+'.mom0.cim')       ; bdps.append(b6[l])
        a6[l] = AT('Mom0',[b5[l]],[b6[l]])
        a6[l].run()

        b7[l] = BDP('Mom0PNG',basename+'.mom0.png')       ; bdps.append(b7[l])
        a7[l] = AT('Mom0PNG',[b6[l]],[b7[l]])
        a7[l].run()

        b8[l] = BDP('fits',basename+'.mom0.fits')        ; bdps.append(b8[l])
        a8[l] = AT('export',[b6[l]],[b8[l]]);
        a8[l].run()

    if False:
        pipeline(bdps)
        a4.set('clip=2')
        pipeline(bdps)

    return bdps

#

#  1000   100   2.5
#   100  1000   3.7

def try3(np=nprojects,nl=nlines):
    print "Nprojects: %d  Nlines: %d" % (np,nl)
    projects = range(np)
    for i in range(np):
        fakename = 'foobar%05d' % (i+1)
        if _debug: print fakename
        projects[i] = ADMIT(fakename)
        projects[i].bdps = try2(nl)
    k = 0
    print "Nprojects: %d  Nlines: %d  k=%d" % (np,nl,k)
    for i in range(np):
        if _debug: print projects[i].bdps[k].updated
        for b in projects[i].bdps:
            b.run()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        try3()
    elif len(sys.argv) > 2:
        np = int(sys.argv[1])
        nl = int(sys.argv[2])
        if len(sys.argv) > 3: _debug = True
        try3(np,nl)
