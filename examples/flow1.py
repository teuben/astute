#! /usr/bin/env python
#
#  Simple data flow using flow (one in, one out)
#
#  In this and subsequent example scripts, various types
#  of ADMIT flow patterns are investigated for correct
#  behavior.
#  1) are dependencies correct for complex flow, does
#     reexecution behave correctly.
#  2) are parameters stored in the correct place
#  3) does XML save and restore state 
#  4) does Pickle do the same

import admit1 as admit

# See also flow1.dot
#digraph flow1 {
#  a1 [shape=box];
#  b0 -> a1 -> b1;
#}


a = admit.ADMIT()

b0 = admit.BDP_file("b0")
b1 = admit.BDP_file("b1")
a1 = admit.AT_flow([b0],[b1])
a1.run()

a.add(b1)

a.pdump('admit1.p')
b0.pdump('b00.p')


