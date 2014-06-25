#
# simple dependency/graph theory of BDP's
# this shows a way to build a dependency tree of BDP's
# @todo the parameter dependence (set via an ADMIT-Task) is not set
# 
# to note:
#    BDP's are generated via an AT, not directly (it needs the associated task)
#    
#

class BDP(object):
    def __init__(self, name='none'):
        self.name    = name
        self.updated = False
        self.deps    = []
        self.derv    = []
        self.task    = None
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
    def run(self):
        if self.updated: 
            print "BDP::%s was up to date" % self.name
            return False
        print "BDP::%s running" % self.name
        if self.task == None:
            print " Warning: no task set ???"
        else:
            # ah, but what about return BDP ???
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
    def __init__(self,bdp_in=[],bdp_out=[],name='none'):
        print "AT(%s)" % name
        self.name    = name
        self.bdp_in  = bdp_in
        self.bdp_out = bdp_out
    def show(self):
        return self.name
    def run(self):
        print "run(%s)" % self.name
        b = BDP('bdp::' + self.name)
        for i in self.bdp_in:
            b.depends_on(i)
        b.task = self
        self.bdp_out.append(b)
        return b
    def rerun(self):
        print "rerun(%s)" % self.name
    def report(self):
        print "AT: ",self.name


bdps = []

#  b0 + b1 -> [a2] -> b2 -> [a3] -> b3
#  also , this doesn't establish filenames
a0 = AT(name='foobar0.fits')     
b0 = a0.run()       ; bdps.append(b0)

a1 = AT(name='foobar1.fits')
b1 = a1.run()                    ; bdps.append(b1)

a2 = AT([b0,b1], [], name='a2')
b2 = a2.run()                    ; bdps.append(b2)
a3 = AT([b2], [], name='a3')
b3 = a3.run()                    ; bdps.append(b3)

for b in bdps:
    print "b-SHOW: ",b.show()

for a in [a2,a3]:
    print "a-SHOW: ",a.show()


for b in bdps:
    print "B:",b.show()
    print "A:",b.task.show()
    # b.task.rerun()
    b.run()

for b in bdps:
    print "B2:",b.show()
    print "A2:",b.task.show()
    # b.task.rerun()
    b.run()
