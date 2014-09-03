#! /usr/bin/env python
#
#  Simple data flow using flow (flow11)
#

import admit1 as admit

a = admit.ADMIT()

b0 = admit.BDP_file("b0")
b1 = admit.BDP_file("b1")
a1 = admit.AT_flow([b0],[b1])
a1.run()

a.add(b1)

a.pdump('admit1.p')
b0.pdump('b00.p')
