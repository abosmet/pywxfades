'''
Created on Jan 7, 2015

@author: Joel
'''
# Standard library from imports
from glob import glob
# Standard library imports
import os
# Module constants
GRIB_STORAGE_PATH = '../../GRIB'
# Begin module code.
def get_available_dates():
    """
    Create a list of available dates by reading the file system.
    Inputs:
     No physical inputs.
    Outputs:
     Returns a list of dates in the form YYYYMMDD (strings).
    """
    # Find items living in the grib storage directory and list them.
    raw_glob = glob(GRIB_STORAGE_PATH + '/*')
    # Loop over all items in the grib storage directory and add the name of the
    #  directory without its path if the item is a directory (Linux only!).
    return [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
#
def get_available_efs_systems(date):
    """
    Create a list of available forecast systems based on the specified date by
     reading the file system.
    Inputs:
     date <string>
      Date in the form YYYYMMDD.
    Outputs:
     Returns a list of available forecast systems in lower-case. i.e. sref
    """
    # Find items living in the grib storage directory, date sub-directory.
    raw_glob = glob(GRIB_STORAGE_PATH + '/' + date + '/*')
    # Loop over all items in the date directory and add the name of the
    #  directory without its path if the item is a directory (Linux only!).
    return [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
#
def get_available_hours(date,system):
    """
    Create a list of available hours based on the specified date and forecast
     system by reading the file system.
    Inputs:
     date <string>
      Date in the form YYYYMMDD
     system <string>
      Forecast system as a lower-case system name. i.e. sref
    Outputs:
     Returns a list of available hours in the form HH (strings).
    """
    # Find items living in the grib storage directory, date sub-directory,
    #  system sub-directory.
    raw_glob = glob(GRIB_STORAGE_PATH + '/' + date + '/' + system + '/*')
    # Loop over all items in the system directory and add the name of the
    #  directory without its path if the item is a directory (Linux only!).
    return [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
#
def get_data_file_list(date,system,hour):
    """
    Creates a list of available data files based on the specified date,
     forecast system, and hour by reading the file system.
    Inputs:
     date <string>
      Date in the form YYYYMMDD
     system <string>
      Forecast system as a lower-case system name. i.e. sref
     hour <string>
      Hour in the form HH
    Outputs:
     Returns a list of files including paths.
    """
    # Find items living in the specified directory and return a list of paths.
    if system == 'sref':
        files = glob(GRIB_STORAGE_PATH + '/' + date + '/' + system + '/' + hour + '/*.grib2')
    elif system == 'gefs':
        files = glob(GRIB_STORAGE_PATH + '/' + date + '/' + system + '/' + hour + '/*.pgrb2*')
    else:
        raise RuntimeError('Invalid system specified. The system was: %s' % (system))
    return files
#
if __name__ == '__main__':
    print 'inventory.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF