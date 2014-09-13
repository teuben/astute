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
b2 = admit.BDP_buckett("b2")

a1  = admit.AT_flow12([b0,b2],[b11,b12])
a1.set('single=1')
a1.run()


a2  = admit.AT_flow12([b11],[b2])
a2.run()

a.add(b0)
a.add(b11)
a.add(b12)
a.add(b2)


a.pdump('flow2b.p')

print "=== TEST1"

#  this will now claim no work is needed because everything is up to date
#  but.....  b2 was updated
a.run()

#  if you then add a signal that a1 was modified:
#  runnning it will run into infinite recursion
#  because of the depenencies recurse
if False:
    a1.set('single=0')

