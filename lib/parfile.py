#! /usr/bin/env python
#
import os

class ParFile(object):
    """read a simple parameter file with key=val , one per line"""
    def __init__(self,file='tas.def',quote=1):
        self.pars={}
        self.quote = quote
        if file == None: return
        self.load(file)
    def load(self,file):
        self.file = file
        if os.path.exists(file):
            f = open(file)
            lines = f.readlines()
            f.close()
        else:
            lines = []
        for line in lines:
            if line[0] == '#': continue
            line0 = line.strip()
            idx = line0.find('=')
            if idx<1: continue
            self.pars[line0[0:idx]] = line0[idx+1:]
    def argv(self,keyvals):
        """merge in key=val, usually from the command line """
        for kv in keyvals:
            idx = kv.find('=')
            if idx<1: continue
            self.pars[kv[0:idx]] = kv[idx+1:]
    def has(self,par):
        return self.pars.has_key(par)
    def get(self,par,alist=False,sep=','):
        if self.pars.has_key(par):
            if alist:
                wl = self.pars[par].split(sep)
                if len(wl) < 2:  return self.pars[par]
                retval = ""
                for w in wl:
                    retval = retval + w + " "
                return retval
            else:
                return self.pars[par]
        else:
            return "-"
    def mgetf(self,par,sep=','):
        ws = self.pars[par].split(sep)
        wf = []
        for w in ws:
            wf.append(float(w))
        return wf
    def mgeti(self,par,sep=','):
        ws = self.pars[par].split(sep)
        wi = []
        for w in ws:
            wi.append(int(w))
        return wi
    def geti(self,par):
        return int(self.pars[par])
    def getf(self,par):
        return float(self.pars[par])
    def set(self,par,val,append=False,sep=','):
        if append:
            if self.pars.has_key(par):
                self.pars[par] = self.pars[par]+sep+val
            else:
                self.pars[par] = val
        else:
            self.pars[par] = val
    def delete(self,par):
        junk = self.pars.pop(par)
    def sort(self,par,sep=','):
        if len(self.pars[par]) > 0:
            val1 = self.pars[par].split(sep)
            val1.sort()
            val2 = ""
            for v in val1:
                if len(val2) == 0:
                    val2 = v
                else:
                    val2 = val2 + sep + v
            self.pars[par] = val2
    def csh(self):
        print "#-BEGIN for c-shell: created by ParFile::"
        for key in self.pars:
            if self.quote==2:
                print "set %s=\"%s\"" % (key,self.pars[key])
            else:
                print "set %s=\'%s\'" % (key,self.pars[key])
        print "#-END"
    def bash(self):
        print "#-BEGIN for bash-shell: created by ParFile::"
        for key in self.pars:
            if self.quote==2:
                print "export %s=\"%s\"" % (key,self.pars[key])
            else:
                print "export %s=\'%s\'" % (key,self.pars[key])
        print "#-END"
    def null(self):
        # nothing for now
        self.null = 1
    def save(self,file=None):
        if file==None:
            f = open(self.file,"w")
        else:
            f = open(file,"w")
        for key in self.pars:
            f.write("%s=%s\n" % (key,self.pars[key]))
        f.close()


if __name__ == '__main__':
    print "No __main__ yet, if ever...."

