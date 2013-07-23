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

setenv LD_PRELOAD "$installpath/lib64/libpython2.6.so $installpath/lib64/libQtCore.so.4.7.1 $installpath/lib64/libQtGui.so.4.7.1 $installpath/lib64/libQtSvg.so.4.7.1 $installpath/lib64/libQtXml.so.4.7.1 $installpath/lib64/libQtDBus.so.4.7.1 $installpath/lib64/libcasacore.so $installpath/lib64/libcfitsio.so.0 $installpath/lib64/libccmtools_local.so $installpath/lib64/libfftw3_threads.so.3 $installpath/lib64/libfftw3f_threads.so.3 $installpath/lib64/libfftw3f.so.3 $installpath/lib64/libfftw3.so.3"

