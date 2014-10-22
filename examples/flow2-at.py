#! /usr/bin/env python
#
#  Simple data flow using flow12 - AT centric version
#
#  b0 -> [b11,b12]
#
import sys, os
import admit2 as admit

a = admit.ADMIT('flow2')


if False:
    # the long version where you see the AT's and ATI's
    a1 = admit.AT_file(name='flow2a')      
    i1 = a.add(a1)
    a1.run()
    
    a2 = admit.AT_flow12('flow2b')       
    i2 = a.add(a2, [(i1,0)])
    a2.run()
else:
    # the compact version where you only see the ATI's
    i1 = a.add(admit.AT_file('flow2a'))
    i2 = a.add(admit.AT_flow12('flow2b'),  [(i1,0)] ) 
    #
    if True:
        print "LEN: ",len(a)
        for i in range(len(a)):
            print "LEN(%d): %s" % (i,a[i].len2())
            a[i].set('touch=1')
    #
    a.run()
    #
    if True:
        # run it again, better not do anything
        print 'Running again'
        a.run()


a.show()
