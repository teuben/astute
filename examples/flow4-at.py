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
    # liberal notation, you can see the AT's, but you do need the ATI's
    # the AT's are in principle not needed, so below
    a1 = admit.AT_file("flow4a")
    i1 = a.add(a1)
    a1.run()

    a2 = admit.AT_flow()                 # this sets the bdp_out's
    i2 = a.add(a2, [(i1,0)] )            # this sets the bdp_in's
    a2.run()

    a3 = admit.AT_flow()
    i3 = a.add(a3, [(i1,0)] )
    a3.run()

    a4 = admit.AT_flow21()
    i4 = a.add(a4, [(i2,0),(i3,0)])
    a4.run()
else:
    # most compact notation, only the ATI's (i1..i4) are needed
    i1 = a.add(admit.AT_file("flow4a") )
    i2 = a.add(admit.AT_flow("flow4b"),     [(i1,0)] )
    i3 = a.add(admit.AT_flow("flow4c"),     [(i1,0)] )
    i4 = a.add(admit.AT_flow21("flow4d"),   [(i2,0),(i3,0)])
    #
    if True:
        print "LEN: ",len(a)
        for i in range(len(a)):
            print "LEN(%d): %s" % (i,a[i].len2())
            a[i].set('touch=1')
    #
    a.run()

a.show()
