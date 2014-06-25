#
# admit tinkertoy, just for a single fits file in the GENERIC telescope model.
#



#  a's   are ADMIT Tasks
#  b's   are BDP's
#  p's   are Parameters


# from ADMIT import *

b1 = BDP('SPWcube','foobar.fits')       # b1 is the input SPWcube where it all starts from
a2 = AT_Summary(b1)
b2 = a2.run()

a3 = AT_CubeStats(b1)
b3 = a3.run(robust=2)                   # b3 is the CubeStats

a4 = AT_LineList(b3)             
b4 = b3.run(min_sigma=4)                # b4 is the LineList

a5 = AT_LineCube(b1,dv=100)             # or should b4 also be input here?
b5 = []                                 # b5[] will be a list of LineCube's
b6 = []                                 # LineCubeStats
b7 = []                                 # LineCubeMom0
for line in b4.getline(0):
    lineName = b4.getLineName(line)
    b5.append(a5.run(b4,line,dv=200))
    a6 = AT_CubeStats(b5[line])
    b6.append(a6.run(robust=3))
    a7 = AT_Moment(b5[line]))
    b7.append(a7.run(moment=0))
    
