#! /usr/bin/env python
#
#  Simple data flow using flow1N - AT centric version
#
#  This version splits 1 BDP into N, and then comnbines them
#  again.   Either N can be known at check time (e.g. if it
#  can be derivedd from the parameters), in which case this
#  can run. 
#  But if N is not known until runtime (you can simulate that
#  with n < 0), the pipeflow cannot be computed without data
#  flowing through it.
#
#  b0 -> [b1,b2,b3,....bN] -> b00
#
import sys, os
import admit2 as admit

a = admit.ADMIT('flowN')

#   set N,  use <0 to simulate that only in runtime can N be determined
n = -4

if True:
    # the more laborious notation

    a1 = admit.AT_file('tmp.flowNa')   
    a1.set('touch=1')
    i1 = a.add(a1)
    a1.run()
    print 'AT[%d]->%s' % (i1,a1.len2())
    
    a2 = admit.AT_flow1N('tmp.flowNb')
    a2.set('n=%d' % n)      
    a2.set('touch=1')
    i2 = a.add(a2, [(i1,0)])

    print 'AT[%d]->%s' % (i2,a2.len2())
    if len(a2) == 0:
        print "*** BAD BAD BAD, a2 no BDP out, need to run first!!"
        a.run()
        print 'AT[%d]->%s' % (i2,a2.len2())
        if len(a2) == 0:
            print "*** BAD BAD BAD, there is no mor rescue for this"

    lot=[]
    for i in range(len(a2)):
        lot.append( (i2,i) )

    a3 = admit.AT_flowN1('tmp.flowNc')
    a3.set('touch=1')
    i3 = a.add(a3, lot)

    print 'AT[%d]->%s' % (i3,a3.len2())

    a.run()

else:
    # the compact notation
    # the flow2,flow4 type doesn't work because of the unknown N at runtime

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
