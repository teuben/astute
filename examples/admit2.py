#
# admit tinkertoy, just for a single fits file in the GENERIC telescope model.
# this is the one that mirrors more like bdp4.py with arbitrary bdp in/out
#


#  a's   are ADMIT Tasks
#  b's   are BDP's
#  p's   are Parameters


# from ADMIT import *

b0 = BDP('fits','foobar.fits')
b1 = BDP('SPWcube','foobar.cim')       # b1 is the input SPWcube where it all starts from
a1 = AT_Ingest([b0],[b1])
a1.run()

b2 = BDP('Summary','foobar.summary')
a2 = AT_Summary([b1],[b2])
a2.run()

b3 = BDP('CubeStats','foobar.cubestats')
a3 = AT_CubeStats([b1],[b3])
a3.run(robust=2)                        # b3 is the CubeStats

b4 = BDP('LineList','foobar.linelist')
a4 = AT_LineList([b3],[b4])             
a4.run(min_sigma=4)                     # b4 is the LineList


nlines = b4.getline(0)
a5 = range(nlines)
b5 = range(nlines)
a6 = range(nlines)
b6 = range(nlines)
b7 = range(nlines)

for l in b4.getline(0):
    lineName = b4.getLineName(line)
    b5[l] = BDP('LineCube',linename)
    a5[l] = AT_LineCube([b1,b4],[b5[l]])
    a5[l].run(dv=200)
    #
    b6[l] = BDP('CubeStats',linename+'.cs')
    a6[l] = AT_CubeStats([b5[l]],b6[l]])
    a6[l].run()

    b7[l] = BDP('Image',linename+'.mom0')
    a7[l] = AT_Moment([b5[l],b6[l]],[b7[l]])
    a7[l].run(mom=0,clip=3)

    # unfinished !!
    
