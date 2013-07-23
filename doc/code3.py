#
# Example code3
#
# use case here is that you have a series of astute enabled directories
# in which you've done all kinds of interesting work, but results
# are stored back in "astute" (astute.xml)
#


import astute

as = astute.Astute()

projects = as.query_dir('.','line(CO)')
np = size(projects)

#  we want to plot L vs. S
s=[]
l=[]

#  loop over the ones found, p is a container for lots of ASTUTE goodies
for p in projects:
    as.setdir(p.name)                # move into the proper project directory
    s.append(p.getpar("s"))
    l.append(p.getpar("l"))
    #
#

