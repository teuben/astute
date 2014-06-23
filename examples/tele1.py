#
# telescope stuff
#
# ALMA:    project, sous, gous, mous
# CARMA:   project, obsblock, subobsblock, trial
# BIMA:
# SMA:     year+semester, project#,       (e.g. 2011B-S048 
#          /rtdc/download-2011/120318_053300_m83_off/RAW/120318_053300.tar.gz 
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

