#! /usr/bin/env python
#
#  Flow with one junction coming back w/ dependency
#
#    /--------- b2 ---\
#  b0 ->  b1           -> b3
#           \ --------/
#
import sys, os
import admit1 as admit

a = admit.ADMIT()

b0 = admit.BDP_file("b0")
a0 = admit.AT_flow([],[b0])
a0.run()

b1 = admit.BDP_file("b1")
a1 = admit.AT_flow([b0],[b1])
a1.run()

b2 = admit.BDP_file("b2")
a2 = admit.AT_flow([b0],[b2])
a2.run()

b3 = admit.BDP_file("b3")
a3 = admit.AT_flow21([b1,b2],[b3])
a3.run()



a.pdump('flow4.p')

