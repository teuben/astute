"""
Utilities for getting computing logs data for containers at the AOS

$Id$
"""
import os
import sys
import distutils.spawn
import shutil
import glob
import datetime

def get_host_name():
    """
    Returns  the  hostname
    """
    hostname = 'http://computing-logs.aiv.alma.cl'
    return  hostname


def get_root_url_for_date(date):
    """
    Returns the root URL of the computing logs web I/F for the given date.

    The argument date should be an ISO-8601 date string (YYYY-MM-DD).
    The returned URL already contains the date.
    """
    year = date[:4]
    mm = date[5:7]
    hostname = get_host_name()
    return "%s/index.php?dir=AOS/CONTAINER/%s/" % (hostname, date)

def get_root_url_for_abm_container(antenna,date):
    """
    Returns the root URL of the computing logs web I/F for the given date.

    The argument date should be an ISO-8601 date string (YYYY-MM-DD).
    The returned URL already contains the date.
    """
    url = get_root_url_for_date(date)
    url += 'alma/logs/' + antenna.lower() + '-abm/CONTROL/' + antenna.upper() + '/' 
    return url

def retrieve_abm_container_data_files(antenna, date, time='*', overwrite=False, verbose=True):
    """
    Retrieve abm container data files via HTTP.

    Parameters are something like:
    antenna = 'DV01'
    container = 'acsStartContainer_cppContainer'
    date = '2010-04-24'  # ISO-8601 date or datetime string

    Return the path to the concatenated file if successful, otherwise '_CURL_FAILED_'.
    """

    isodate = get_datetime_from_isodatetime(date).date().strftime('%Y-%m-%d')
    inputdate = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    rooturl = get_root_url_for_abm_container(antenna,date)

    today = datetime.datetime.today()
    twentydaysago = today + datetime.timedelta(days=-20)

    unzip = 1
    extension = 'txt.gz'

    completeurl = '%s' % (rooturl)
    completeurl = completeurl.replace('index.php?dir=','')
    directory = completeurl.replace('http://','')
    print completeurl
    if (os.path.exists(directory) == False or overwrite):
        print "Retrieving %s" % (completeurl)
        wget = distutils.spawn.find_executable('wget',path=':'.join(sys.path)+':'+os.environ['PATH'])
        cmd = wget + ' -r -l1 --no-parent -A.gz %s' % (completeurl) # -o %s' % (completeurl, outfile)
        # will write to new subdirectory: computing-logs.aiv.alma.cl/AOS/CONTAINER/2014-04-29/alma/logs/dv25-abm/CONTROL/DV25/
        print "Calling: ", cmd
        exitcode = os.system(cmd)
        if exitcode == 0:
            if  unzip:
                files = glob.glob(directory+'/*.gz')
                for f in files:
                    os.system('gunzip -f %s' %f)
                files = glob.glob(directory+'/*')
                for f in files:
                    if (f.find('.tar') >= 0):
                        os.system('tar -C %s -xvf %s' % (directory,f))
                        os.remove(f)
            files = sorted(glob.glob(directory+'/*'))
            print files
            allfiles = catAllFiles(files, outfilename=files[0][:-13]) # strip off the time string at end
            print "concatenated file = ", allfiles
            return allfiles
        else:
            print 'Retrieval failed. Check permissions on directory and set outpath if necessary'
            return '_CURL_FAILED_'
    else:
        files = sorted(glob.glob(directory+'/*'))
        if (verbose):
            print "Directory already present, returning name of file: ", files[0]
        return files[0]

def catAllFiles(files, outfilename='allfiles', remove=True):
    with open(outfilename, 'wb') as outfile:
        for filename in files:
            with open(filename) as readfile:
                shutil.copyfileobj(readfile, outfile)
            if (remove):
                os.remove(filename)
    return(outfilename)

def get_datetime_from_isodatetime(isodatetime):
    """
    Return a datetime.datetime object for given ISO-8601 date/datetime string.

    The argument isodatetime should be in YYYY-MM-DDThh:mm:ss or YYYY-MM-DD
    (in the latter case, 00:00:00 is assumed).
    Return 0001-01-01T00:00:00 if an invalid string is given.
    """

    datelist = isodatetime.split('T')
    if len(datelist) == 1:  # date only
        timelist = [0, 0, 0]
        datelist = datelist[0].split('-')
    elif len(datelist) == 2:  # date and time
        timelist = datelist[1].split(':')
        datelist = datelist[0].split('-')
    else:
        print "Date %s is invalid." % isodatetime
        return datetime.date(1, 1, 1)

    if (len(datelist) == 3) and (len(timelist) == 3):
        microsec = int(1e6 * (float(timelist[2]) - int(float(timelist[2]))))
        timelist[2] = int(float(timelist[2]))
        return datetime.datetime( \
            int(datelist[0]), int(datelist[1]), int(datelist[2]), \
            int(timelist[0]), int(timelist[1]), int(timelist[2]), microsec )
    else:
        print "Date '%s' is invalid." % isodatetime
        return datetime.date(1, 1, 1)
