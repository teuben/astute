#
# simple dependency/graph theory of BDP's
#

class bdp(object):
    def __init__(self, name='one'):
        self.name    = name
        self.updated = False
        self.deps    = []
        self.derv    = []
    def show(self):
        return self.name
    def update(self,new_state):
        print "UPDATE: %s" % self.name
        self.updated = new_state
        for d in self.derv:
            d.update(new_state)
    def depends_on(self,other):
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
    def run(self):
        if self.updated: 
            print "BDP::%s was up to date" % self.name
            return False
        print "BDP::%s running" % self.name
        self.updated = True
        return True

def DependsOn(a,b):
    """ b depends on a """
    b.depends_on(a)
    


# make some kind of container, a list in this case.
bdps = []

# create a few in the initial ADMIT pipeline
SPWcube       = bdp('SPWcube')          ; bdps.append(SPWcube)
Summary       = bdp('Summary')          ; bdps.append(Summary)
Summary.depends_on(SPWcube)
CubeStats     = bdp('CubeStats')        ; bdps.append(CubeStats)
CubeStats.depends_on(SPWcube)
LineList      = bdp('LineList')         ; bdps.append(LineList)
LineList.depends_on(CubeStats)
LineCube      = bdp('LineCube')         ; bdps.append(LineCube)
LineCube.depends_on(LineList)
LineCubeStats = bdp('LineCubeStats')    ; bdps.append(LineCubeStats)
LineCubeStats.depends_on(LineCube)


# Take the 2nd route via PV diagram
if True:
    CubeMom0      = bdp('CubeMom0')     ; bdps.append(CubeMom0)
    CubeMom0.depends_on(CubeStats)
    PosVelMap     = bdp('PosVelMap')    ; bdps.append(PosVelMap)
    PosVelMap.depends_on(CubeMom0)
    XCorrList     = bdp('XCorrList')    ; bdps.append(XCorrList)
    XCorrList.depends_on(PosVelMap)
    LineList.depends_on(XCorrList)


#
LC_1  = bdp('LC_1')                     ; bdps.append(LC_1)
LC_1.depends_on(LineCube) 
LC_1_m0 = bdp('LC_1_m0')                ; bdps.append(LC_1_m0)
LC_1_m0.depends_on(LC_1)



# here you can play with 
SPWcube.update(True)
XCorrList.update(False)


# run them all
for i in bdps:
    i.run()



# report
if False:
    for i in bdps:
        i.report()

