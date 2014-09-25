#! /usr/bin/env python
#
#  Simple data flow using flow1N - AT centric version
#
#  b0 -> [b1,b2,b3,....bN]
#
import sys, os
import admit2 as admit

a = admit.ADMIT('flowN')


if True:
    a1 = admit.AT_file('tmp.flowNa')   
    a1.set('touch=1')
    i1 = a.add(a1)
    a1.run()
    
    a2 = admit.AT_flow1N('tmp.FlowNb')
    a2.set('n=4')
    a1.set('touch=1')
    a2.run()
    i2 = a.add(a2, [(i1,0)])
else:
    i1 = a.add(admit.AT_file('tmp.flowNa'))
    i2 = a.add(admit.AT_flow1N('tmp.flowNb'),  [(i1,0)] ) 
    #
    a.run()
    #
    if True:
        print "LEN: ",len(a)
        for i in range(len(a)):
            print "LEN(%d): %s" % (i,a[i].len2())
            a[i].set('touch=1')
    #


a.show()
