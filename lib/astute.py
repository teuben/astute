#! /usr/bin/env python
#
#  Initialize various useful tihngs for ASTUTE
#
#  1) find out what environment we have and what packages we have
#  2) provide easy interfaces to run alien packages (shell, idl)


import sys, os
import runsh, runidl


class Astute(object):
    """
    assert an ASTUTE environment
    """
    def __init__(self,verbose=False):
        self.n = 0
        self.have={}
        self.version="29-may-2013"
        if os.environ.has_key('ASTUTE'):
            self.have['ASTUTE'] = os.environ['ASTUTE']
        if os.environ.has_key('NEMO'):
            self.have['NEMO']   = os.environ['NEMO']
        if os.environ.has_key('MIR'):
            self.have['MIRIAD'] = os.environ['MIR']
        # CASA is a bit tricky, may not exist in shell, but will in casapy
        if os.environ.has_key('CASAPATH'):
            self.have['CASA'] = os.environ['CASAPATH'].split()[0]
        elif os.environ.has_key('CASADATA'):
            self.have['CASA'] = os.environ['CASADATA']
        if not self.have.has_key('CASA'):
            for p in os.environ['PATH'].split(':'):
                t = p+'/casapy'
                if os.path.isfile(t):
                    self.have['CASA'] = p
                    print "found ",t
                    break
        have = ""
        if self.have.has_key('ASTUTE'):  have = have + "ASTUTE "
        if self.have.has_key('NEMO'):    have = have + "NEMO "
        if self.have.has_key('MIRIAD'):  have = have + "MIRIAD "
        if self.have.has_key('CASA'):    have = have + "CASA "

        self.x = runsh.shell()
        self.idl = runidl.IDL()
            
        print "Astute (version %s) initialized [%s]" % (self.version,have.strip())
    def has(self,name):
        #print "ASTUTE: testing for %s: %s" % (name, self.have.has_key(name))
        return self.have.has_key(name)

    def need(self,names):
        bad = 0
        for n in names:
            if not self.have.has_key(n):
                print "ASTUTE: %s not present" % n
                bad = bad + 1
        if bad:
            raise RuntimeError
    def nemo(self,cmdline):
        self.x.run(cmdline.split())
    def miriad(self,cmdline):
        self.x.run(cmdline.split())
    def shell(self,cmds):
        self.x.run(cmds)
    def idl(self,cmds):
        self.idl.run(cmds)
        
        
if __name__ == "__main__":
    a = Astute()
    a.has('NEMO')
    a.has('MIRIAD')
    a.need(['NEMO','MIRIAD'])
    if a.has('NEMO'):
        a.shell(['tsf','help='])
        # a.shell('tsf help=')
