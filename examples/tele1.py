#
# telescope stuff
#
# ALMA:    project, sous, gous, mous
# CARMA:   project, obsblock, subobsblock, trial
# BIMA:
# GENERIC: project

class tel(object):
    def __init__(self, name='one'):
        self.name    = name
    def show(self):
        return self.name
    def report(self):
        print "===report==="
        print "TEL::%s" % self.name

# make some kind of container, a list in this case.
tels = []

