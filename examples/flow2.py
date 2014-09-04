#! /usr/bin/env python
#
#  Simple data flow using flow12
#
#  b0 -> [b11,b12]
#
import sys, os
import admit1 as admit

a = admit.ADMIT()

b0 = admit.BDP_file("b0")
a0 = admit.AT_file([],[b0])
a0.run()

b11 = admit.BDP_buckett("b11")
b12 = admit.BDP_buckett("b12")
a1  = admit.AT_flow12([b0],[b11,b12])
a1.run()


a.add(b0)
a.add(b11)
a.add(b12)


a.pdump('flow2.p')

