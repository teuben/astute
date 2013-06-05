#! /bin/csh -f
#
#  terrible example how to bootstrap a project, but we have to
#  live with the decision of the naming convention

set in   = "ngc253_fullcube_%s_SPW_%d_contsub_clean.fits"
set out  = "w_%d_%s"

set configuration = ("extended" "compact")
set spw           = (0 1 2 3)


set dirs=$TAS/etc/n253.dir

# boostrap can only runs once
piperun -c $dirs 'pipeset -c project=%s'
piperun    $dirs 'cat $TAS/etc/n253.tas.def >> tas.def'

# this complex loop is needed because of the peculiar name convention we opted for
foreach c ($configuration)
  foreach s ($spw)
    set c1=`echo $c | cut -c1`
    set dir=w_${s}_${c1}
    set fits=`printf $in $c $s` 
    (cd $dir ; ls -l; echo $fits; pipeset 'fits=$TAS/rawdata/n253/'$fits)
  end
end

# save it for all others to have an easier life
piperun    $dirs  pipesave
# and might as well get all the symlinks set up right away
piperun    $dirs  pipesetup project=%s
