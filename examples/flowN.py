#! /usr/bin/env python
#
#  Simple data flow using flow12
#
#  b0 -> [b1,b2,b3,....bN]
#
import sys, os
import admit1 as admit

a = admit.ADMIT('flow2')

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
a1.set('debug=1')
a.run()
for b in a.bdps:
    print b.filename,b.task[0],b.task[0].name

a.show()


#  now an example how you can reconstruct;
#  this is pickle specific though,not XML

aa = a.pload('flow2.p')

#  running it of course will need no work.
aa.run()


#  print out the tasks, notice that FLOW12 now has two different addressed... it should not !!
#  this is a pickle side-effect
for b in aa.bdps:
    print b.filename,b.task[0],b.task[0].name




# 
print "===TEST1"
b11.updated = False
b11.run()

print "===TEST2"

b11.run()


print "===TEST3"
a1.set('debug=0')
a1.run()
