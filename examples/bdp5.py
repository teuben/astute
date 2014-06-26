#
# simple dependency/graph theory of BDP's
# this shows a way to build a dependency tree of BDP's
# 
# to note:
#    BDP's are always needed as input/output for an AT, they will
#    then be contained within an AT
#    
#

class BDP(object):
    def __init__(self, name='none', filename='foobar'):
        self.name    = name
        self.updated = False
        self.deps    = []
        self.derv    = []
        self.task    = None
        print "BDP(%s) " % name
    def show(self):
        return self.name
    def update(self,new_state):
        print "UPDATE: %s" % self.name
        self.updated = new_state
        for d in self.derv:
            d.update(new_state)
    def depends_on(self,other):
        if other == None: return
        print 'BDP %s depends on %s' % (self.name,other.show())
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
        print "BDP::set %s" % keyval
    def run(self):
        if self.updated: 
            print "BDP::%s was up to date" % self.name
            return False
        print "BDP::%s running" % self.name
        if self.task == None:
            print " Warning: no task set ???"
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
        print "AT.init(%s)" % name
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
        print "AT.run(%s)" % self.name
        do_nothing = True
        for b2 in self.bdp_out:
            if not b2.updated: do_nothing = False
        if do_nothing:
            print "   no work needed here"
            return False
        for b2 in self.bdp_out:
            b2.updated = True
        return True
    def set(self,keyval):
        for b2 in self.bdp_out:
            if b2.updated:
                b2.update(False)
    def rerun(self):
        print "AT.rerun(%s)" % self.name
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
        print "AT_ingest.init"
    def run(self):
        print "AT_ingest.run"
        if not AT.run(self):
            return False
        # specialized work can commence here



class AT_combine(AT):
    name = 'COMBINE'
    version = '1.0'
    keys = []
    def __init__(self,bdp_in=[],bdp_out=[]):
        AT.__init__(self,self.name,bdp_in,bdp_out)
        print "AT_combine.init"
    def run(self):
        print "AT_combine.run"
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
        print "AT_flow.init"
        AT.__init__(self,self.name,bdp_in,bdp_out)
    # note the deliberate bug to not implement the .run() here


bdps = []

def pipeline(bdps):
    print "===============   Running pipeline ============="
    for b in bdps:
        b.run()


def try1(do_show=True, do_dep=True):
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

def try2():
    b0 = BDP('fits','foobar.fits')         ; bdps.append(b0)
    b1 = BDP('SPWcube','foobar.cim')       ; bdps.append(b1)
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

    # these onward can be indexed if  > 1 line
    b5 = BDP('LineCube','foobar.CO.cim')       ; bdps.append(b5)
    a5 = AT('LineCube',[b1,b4],[b5])
    a5.set('dv=100')
    a5.run()
    
    b6 = BDP('Mom0','foobar.CO.mom0.cim')       ; bdps.append(b6)
    a6 = AT('Mom0',[b5],[b6])
    a6.run()
    
    b7 = BDP('Mom0PNG','foobar.CO.mom0.png')       ; bdps.append(b7)
    a7 = AT('Mom0PNG',[b6],[b7])
    a7.run()

    #
    pipeline(bdps)
    a4.set('clip=2')
    pipeline(bdps)
    
    

#try1()
try2()
