#! /usr/bin/env python
#

import os, sys


try:
    import astropy
    print "astropy OK"
except:
    print "no astropy"
    sys.exit(0)

try:
    from astropy.table import Table
except:
    print "astropy.table MISSING"
    sys.exit(0)


fno =  'test_astropy_table.tab'
print "Testing astropy.table",fno

 
a = [1, 4, 5]
b = [2.0, 5.0, 8.2]
c = ['x', 'y', 'z']
t = Table([a, b, c], names=('a', 'b', 'c'), meta={'name': 'first table'})
print t
t.write(fno,format='ascii.commented_header')
