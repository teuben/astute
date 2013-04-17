#! /usr/bin/env python
#
#
# gdl (or idl)
# >> .run clfind
# >> clfind,file='../example/rosette',low=0.5,inc=0.5,/log
# exit

import sys,os
from subprocess import Popen, PIPE, STDOUT

class IDL(object):
    def __init__(self,name='gdl'):
        if name == 'gdl':
            # poor man's checker
            # check if /usr/bin/gdl exists, if not, use idl :-(
            if not os.path.exists("/usr/bin/gdl"):
                print "Warning: gdl not available, switching to idl"
                name = 'idl'
        self.name = name
        self.cmd = [name]
        print "IDL(%s)" % name
    def show(self):
        return self.name
    def setcmd(self,cmd):
        """ only for other testing, as this will override the command
        """
        self.cmd = cmd
    def addpath(self,path):
        """ add to the IDL_PATH or GDL_PATH environment
        """
    def run(self,cmds):
        print "RUN %s" % self.cmd
        p = Popen(self.cmd,stdout=PIPE,stdin=PIPE,stderr=PIPE)
        cmd = ""
        for c in cmds:
            print "CMD: ",c
            cmd=cmd+'%s\n' % c
        # print cmd
        if False:
            a1=p.stdin.write(cmd)
            a2=p.communicate()
            print a2
        else:
            lines = p.communicate(input=cmd)
            p.stdin.close()
            for line in lines:
                print line
        
if __name__ == "__main__":
    # testing
    x = IDL()
    print "SHOW: ",x.show()
    cmds=['print,1','print,1+1']
    x.run(cmds)
    #
    if False:
        x.setcmd(['grep','f'])
        x.run(['one','two','three','four','five','six'])
