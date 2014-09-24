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

a = admit.ADMIT()


a1 = admit.AT_file()      ; a.add(a1)
a1.set("file=foobar.fits")
a1.run()                                    # a1[0] is now the BDP (b0)


a2 = admit.AT_flow([a1[0]]) ; a.add(a2)
a2.run()                                    # a2[0] is the BDP out (b1)

a3 = admit.AT_flow([a1[0]]) ; a.add(a3)
a3.run()                                    # a3[0] is the BDP out (b2)

a4 = admit.AT_flow21([a2[0],a3[0]]) ; a.add(a4)
a4.run()                                    # a4[0] is the BDP out (b3)

