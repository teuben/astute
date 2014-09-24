#! /usr/bin/env python
#
#  Simple data flow using flow12 - AT centric version
#
#  b0 -> [b11,b12]
#
import sys, os
import admit2 as admit

a = admit.ADMIT('flow2')


a1 = admit.AT_file()      ; a.add(a1)
a1.set("file=foobar.fits")
a1.run()                                    # a1[0] is now the BDP (b0)


a2  = admit.AT_flow12([ a1[0] ]) ; a.add(a2)
a2.run()                                    # a2[0] and a2[1] are now the BDP's (b11,b12)


