#! /bin/csh -f
#
#   unix shell example how an ASTUTE pipeline for N253 works
#   appr. time of these 5 steps:  1" + 1' + 7' + 4' + 2" ~ 12'

set log=n253_pipe.log
set n=1

# report/remind if ASTUTE was loaded with enough components
astute

# run the pipeline
echo -n "SETUP: "
time piperun -c n253.dir pipesetup project=%s              >& $log.$n ; @ n++
echo -n "GETDATA: "
time piperun    n253.dir getdata                           >& $log.$n ; @ n++
#echo -n "CUBESTATS_NEMO: "
#time piperun    n253.dir cubestats_nemo                   >& $log.$n ; @ n++
echo -n "LINE_ID: "
time piperun    n253.dir line_id                           >& $log.$n ; @ n++
echo -n "LINE_ID_NEMO: "
time piperun    n253.dir line_id_nemo                      >& $log.$n ; @ n++

