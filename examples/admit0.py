#
# admit tinkertoy
#


class Project(object):
    def __init__(self,name):
        self.name = name
        self.source = {}

class Source(object):
    def __init__(self,name):
        self.name = name
        self.band = {}
        self.line = {}

class Band(object):
    def __init__(self,name):
        self.name = name

class Line(object):
    def __init__(self,name,freq,p=1.0):
        self.name = name
        self.freq = freq


p1 = Project('p1')
s1 = Source('s1')
s2 = Source('s2')
s3 = Source('s3')
b1 = Band('1')
b2 = Band('2')
b3 = Band('3')
b4 = Band('4')
l1 = Line('co',115.27)
l2 = Line('hcn',88.21)

p1.source[s1.name] = s1  # deeper
p1.source[s2.name] = s2
p1.source[s3.name] = s3

s1.band[b1.name] = b1  # deeper
s1.band[b2.name] = b2
s1.band[b3.name] = b3
s1.band[b4.name] = b4

s1.line[l1.name] = l1  # deeper
s1.line[l2.name] = l2

ns = len(p1.source)
nb = len(s1.band)
nl = len(s1.line)

print p1.name,' has ', len(p1.source), ' sources:'
for s in p1.source.keys():
    print s
# notice both return the same number
print 's1 #bands:', len(s1.band)
for s in p1.source.keys():
    print '%s #bands:%d' % ( s , len(p1.source[s].band))

