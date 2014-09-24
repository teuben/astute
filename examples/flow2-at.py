#! /usr/bin/env python
#
#  Simple data flow using flow12 - AT centric version
#
#  b0 -> [b11,b12]
#
import sys, os
import admit2 as admit

a = admit.ADMIT('flow2')


a1 = admit.AT_file('name=flow2')   
i1 = a.add(a1)
a1.run()

a2 = admit.AT_flow12()
i2 = a.add(a2, [(i1,0)])
a2.run()


a.show()
