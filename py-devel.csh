# 
# source this file to modify your environment for some forms of python development
#
# see also: http://kneedme.blogspot.com/2011/09/install-additional-modulespackages-in_22.html
#

if ($?CASAPATH == 0) then
   echo no CASAPATH
   exit
endif
set cp=(`echo $CASAPATH`)

set installpath=$cp[1]

setenv LD_LIBRARY_PATH  $installpath/lib64:/lib64:/usr/lib64:$LD_LIBRARY_PATH
setenv CASAPATH  "$installpath `uname -s | tr '[:upper:]' '[:lower:]'` local `uname -n`"
setenv PATH  "$installpath/lib64/exec:$installpath/lib64/casapy/bin:/usr/bin:/usr/X11R6/bin:$PATH"

setenv MATPLOTLIBRC    "$installpath/share/matplotlib"
setenv PYTHONHOME      $installpath

if ($?PYTHONPATH) then
  setenv _PYTHONPATH      $PYTHONPATH
  setenv PYTHONPATH $installpath/lib64/python2.6:$installpath/lib64/python2.6/heuristics:$installpath/lib64/python2.6/site-packages:$_PYTHONPATH
else
  setenv PYTHONPATH $installpath/lib64/python2.6:$installpath/lib64/python2.6/heuristics:$installpath/lib64/python2.6/site-packages
endif

setenv TCL_LIBRARY         "$installpath/share/tcl8.4"
setenv QT_PLUGIN_PATH      "$installpath/lib64/qt-4.7.1/plugins"
setenv __CASAPY_PYTHONDIR  "$installpath/lib64/python2.6"

setenv PGPLOT_FONT $installpath/lib64/pgplot/grfont.dat
setenv PGPLOT_DIR  $installpath/lib64
setenv PGPLOT_RGB  $installpath/lib64/pgplot/rgb.txt


set _lib=$installpath/lib64

setenv LD_PRELOAD "$_lib/libpython2.6.so $_lib/libQtCore.so.4.7.1 $_lib/libQtGui.so.4.7.1 $_lib/libQtSvg.so.4.7.1 $_lib/libQtXml.so.4.7.1 $_lib/libQtDBus.so.4.7.1 $_lib/libcasacore.so $_lib/libcfitsio.so.0 $_lib/libfftw3_threads.so.3 $_lib/libfftw3f_threads.so.3 $_lib/libfftw3f.so.3 $_lib/libfftw3.so.3"

unset _lib
