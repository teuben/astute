#! /usr/bin/env python
#
# Testing Flow Manager
#

import sys, os
import FlowManager as FM
import admit2 as admit


fm = FM.FlowManager()

## flow4
#      /--a0--\
#    a1        a2
#      \--a3--/

fm.connmap = [(0, 0, 1, 0), (0, 0, 2, 0), (1, 0, 3, 0), (2, 0, 3, 1)]
#fm.connmap = [("a0", 0, "a1", 0), ("a0", 0, "a2", 0), ("a1", 0, "a3", 0),("a2", 0, "a3", 1)]

print fm.connmap;

a0 = admit.AT_file("a0")
fm.tasks[a0.taskid]=a0

a1 = admit.AT_file("a1")
a1.bdp_in.append(a0[0])
fm.tasks[a1.taskid]=a1

a2 = admit.AT_file("a2")
a2.bdp_in.append(a0[0])
fm.tasks[a2.taskid]=a2

a3 = admit.AT_file("a3")
a3.bdp_in.append(a1[0])
a3.bdp_in.append(a2[0])
fm.tasks[a3.taskid]=a3

## test insert method
a4 = admit.AT_file("a4")
fm.insert(a4,0, (0, 0, 2, 0))
print fm.connmap
for key in fm.tasks:
    print key, ":", fm.tasks[key].name

# f = fm.findroots()
# if len(f) > 0:
#     print f
#     for node in f:
#         print node
#         print node[0]
# v = fm.verify()
# d = fm.makedepsmap()