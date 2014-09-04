#! /usr/bin/env python
#
#  Simple data flow using flow21
#
#  [b01,b02] -> b1
#
import sys, os
import admit1 as admit

a = admit.ADMIT()


#  here we create a01 and a02, but in theory one should be
#  able to use just a0 and reuse it, but there probably is
#  a bug (or feature) in the state of the AT's. 
#  This should be checked out!

b01 = admit.BDP_file("b01")
a01 = admit.AT_file([],[b01])
a01.run()

b02 = admit.BDP_file("b02")
a02 = admit.AT_file([],[b02])
a02.run()


b1 = admit.BDP_buckett("b1")
a1 = admit.AT_flow21([b01,b02],[b1])
a1.run()


a.add(b01)
a.add(b02)
a.add(b1)


a.pdump('flow3.p')

