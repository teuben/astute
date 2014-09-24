#! /usr/bin/env python
#
#  Flow with one junction coming back w/ dependency
#
#      /--b1--\
#    b0        b3
#      \--b2--/
#
import sys, os
import admit2 as admit

#   import admit.AT_casa as AT
#   a1 = AT.ingest('foobar.fits')



a = admit.ADMIT()

if False:
    a1 = admit.AT_file("flow4")
    i1 = a.add(a1)
    a1.run()

    a2 = admit.AT_flow()
    i2 = a.add(a2, [(i1,0)] )
    a2.run()

    a3 = admit.AT_flow()
    i3 = a.add(a3, [(i1,0)] )
    a3.run()

    a4 = admit.AT_flow21()
    i4 = a.add(a4, [(i2,0),(i3,0)])
    a4.run()
else:
    i1 = a.add(admit.AT_file("flow4"))
    i2 = a.add(admit.AT_flow(),             [(i1,0)] )
    i3 = a.add(admit.AT_flow(),             [(i1,0)] )
    i4 = a.add(admit.AT_flow21(),           [(i2,0),(i3,0)])
    a[i4].set('a=1')

    a.run()

print i1,i2,i3,i4

a.show()
