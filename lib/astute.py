#! /usr/bin/env python
#
#  Initialize various useful tihngs for ASTUTE
#
#  1) find out what environment we have and what packages we have
#


import sys, os


class Astute(object):
    """
    assert an ASTUTE environment
    """
    def __init__(self):
        self.n = 0
        self.astute = os.environ.has_key('ASTUTE')
        self.nemo   = os.environ.has_key('NEMO')
        self.miriad = os.environ.has_key('MIR')
        self.casa   = os.environ.has_key('CASADATA')
        if not self.casa:
            for p in os.environ['PATH'].split(':'):
                t = p+'/casapy'
                if os.path.isfile(t):
                    self.casa = True
                    print "found ",t
                    break
        have = ""
        if self.astute:  have = have + "ASTUTE "
        if self.nemo:    have = have + "NEMO "
        if self.miriad:  have = have + "MIRIAD "
        if self.casa:    have = have + "CASA "

            
        print "Astute initialized [%s]" % have
    def has(self,name):
        print "ASTUTE: testing for %s" % name
        print os.environ.has_key(name)
    
        
        
        
if __name__ == "__main__":
    a = Astute()
    a.has('NEMO')
    a.has('MIRIAD')

