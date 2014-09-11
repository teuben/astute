#! /usr/bin/env python
#
#  Flow with one junction coming back w/ dependency
#
#      /--b1--\
#    b0        b3
#      \--b2--/
#
import sys, os
import admit1 as admit

a = admit.ADMIT()

b0 = admit.BDP_file("b0")
a0 = admit.AT_flow([],[b0],'a0')
a0.run()

b1 = admit.BDP_file("b1")
a1 = admit.AT_flow([b0],[b1],'a1')
a1.run()

b2 = admit.BDP_file("b2")
a2 = admit.AT_flow([b0],[b2],'a2')
a2.run()

b3 = admit.BDP_file("b3")
a3 = admit.AT_flow21([b1,b2],[b3],'a3')
a3.run()

a.add(b0)
a.add(b1)
a.add(b2)
a.add(b3)

a.pdump('flow4.p')

print "DONE==========================================="
a2.set("debug=0")
a.run()
print "ALL DONE==========================================="


#  now an example how you can reconstruct;
#  this is pickle specific though,not XML

aa = a.pload('flow4.p')

#  running it of course will need no work.
aa.run()


#  print out the tasks, notice that 
for b in aa.bdps:
    print b.filename,b.task[0],b.task[0].name





#
"""

testing with a user interface:

1) pickle form

   a) create from scratch, if flow4.p not present; no options parsed
   b) if flow4.p present, read and instatiate the a's and b's.
      - rerun pipeline should cause no work to be done
      - set a parameter anywhere in the a0,a1,a2,a3 and re-run pipeline


"""
