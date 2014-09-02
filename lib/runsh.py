#! /usr/bin/env python
#
#

import sys, os
from subprocess import Popen, PIPE, STDOUT
import subprocess

class shell(object):
    def __init__(self,name='sh'):
        """ 
        nothing needed here
        """
        self.name = name
        # print "SH(%s)" % name
    def show(self):
        return self.name
    def run0(self,cmds):
        cmd = cmds[0]
        for c in cmds[1:]:
            cmd = cmd + " " + c
        subprocess.call(cmd, shell=True)
    def run(self,cmds):
        cmd = cmds[0]
        for c in cmds[1:]:
            cmd = cmd + " " + c
        fp = os.popen(cmd,'r')
        lines = fp.readlines()
        fp.close()
        for line in lines:
            print line.strip()

if __name__ == "__main__":
    # testing
    x = shell()
    print "SHOW: ",x.show()
    cmds=['ls','-l']
    x.run(cmds)
