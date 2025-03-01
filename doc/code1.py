#
# ASTUTE hypothetical example
#
# use case: start with an archive query, and grab data as well, as needed
#

import astute

line=[-200, 200, 10]

as = astute.Astute()
ar = astute.Archive()

projects = ar.query('gal && line(CO) && z<0.2 && T>1')
np = size(projects)

for p in projects:
    as.setdir(p.name)                 # move into the proper directory
    nc = size(p.cubes)
    for c in p.cubes:                 # project 'p' and a series of 'c' cubes
        x = p.grab('x')
        if x.hasline('co'):
            f = p.grab('fits')
            as.importfits(f)         # this writes a MS
            as.regridvel(f,line)
            rms = x.get_rms(line)
            as.moment0(f)
        #
    #
#
