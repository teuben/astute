"""
Telescope Type class

ALMA:    project, sous, gous, mous
CARMA:   project, obsblock, subobsblock, trial
BIMA:    project, id, trial, date.raw(eg 00aug15.raw), source(eg, mars.tar)
VLA:     project
GENERIC: project

"""

class TelescopeType:

    name = ''
    types = ['ALMA', 'CARMA', 'BIMA', 'VLA', 'DENERIC']
    container = None

    def __init__(self): pass
    
    def setVal(self, name=None, val=None):
        self.name = name
        self.container = dict(val)

    def getName(self):
        return self.name

    def report(self):
        print "===report==="
        print "Telescope:", self.name

        for id, val in self.container.iteritems():
            print id, '=', val

### Test #####
# name = "ALMA"
# ids = [('project', '2012.1.01234.S'),('sous', 'A000_X01_X00'), ('gous', 'A000_X01_X01'), ('mous', 'A000_X01_Xxx1')]
# 
# tel = TelescopeType()
# tel.setVal(name, ids)
# print "Telescope name:", tel.getName()
# tel.report()
