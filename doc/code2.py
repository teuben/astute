#
# Example: code2
#
# In a currently astute activated code
#


import astute

line=[-200, 200, 10]

as = astute.Astute()
ar = astute.Archive()

#  search here and below for astute.xml files
#  optionally a query for science, e.g. only CO lines
projects = as.query_dir('.','line(CO)')
np = size(projects)

#  loop over the ones found, p is a container for lots of ASTUTE goodies
for p in projects:
    as.setdir(p.name)                # move into the proper directory
    nc = size(p.cubes)
    for c in p.cubes:
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
