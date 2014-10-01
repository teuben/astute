import sys, os
import casa, taskinit
import admit2 as admit

class AT_export(admit.AT):
    name    = 'EXPORT'
    version = '1.0'
    keys    = []
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        n=0
        # there will be no BDP out
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        self.bdp_out = []
        for b in self.bdp_in:
            fni = b.filename
            fno = fni + '.fits'
            casa.exportfits(fni,fno,overwrite=True)
        # done.
