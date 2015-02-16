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
# Available runs to be populated on package import.
available_runs = []
# Begin module code.
def gen_available_runs():
    """
    Uses glob to find available model runs in the grib storage directory.
    Inputs:
        No physical inputs.
    Outputs:
        No physical outputs. Sets a module-level variable.
    """
    # Get a list of all directories matching the storage pattern.
    folders = glob(GRIB_STORAGE_PATH + '/[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0'\
                   '-9]/*/[0-9][0-9]')
    # Construct tuples with information about each path.
    for folder in folders:
        path = folder
        split_path = folder.split('/')
        date_str, hour_str = split_path[-3], split_path[-1]
        system = split_path[-2]
        if system == 'sref':
            num_files = len(glob('{0}/*.grib2'.format(path)))
        elif system == 'gefs':
            num_files = len(glob('{0}/*.pgrb2*'.format(path)))
        else:
            raise RuntimeError('Invalid system in storage directory! The syste'\
                               'm was: %s' % (system))
        desc = '{0}-{2}-{4}\t{5}Z\t{1}\t{3}'.format(date_str[0:4], system,
                                                    date_str[4:6], num_files,
                                                    date_str[6:8], hour_str)
        run = (path, desc)
        available_runs.append(run)
    return
#
def get_available_dates():
    """
    Create a list of available dates by reading the available runs.
    Inputs:
     No physical inputs.
    Outputs:
     Returns a list of dates in the form YYYYMMDD (strings).
    """
    # Loop over items in available runs and add the date portion (index -3).
    return [i[0].split('/')[-3] for i in available_runs if os.path.isdir(i[0])]
#
def get_available_efs_systems(date):
    """
    Create a list of available forecast systems based on the specified date by
     reading the available runs.
    Inputs:
     date <string>
      Date in the form YYYYMMDD.
    Outputs:
     Returns a list of available forecast systems in lower-case. i.e. sref
    """
    # Loop over items in available runs and add the system portion for matching
    #  dates.
    return [i[0].split('/')[-2] for i in available_runs if\
             os.path.isdir(i[0]) and i[0].split('/')[-3] == date]
#
def get_available_hours(date,system):
    """
    Create a list of available hours based on the specified date and forecast
     system by reading the available dates.
    Inputs:
     date <string>
      Date in the form YYYYMMDD
     system <string>
      Forecast system as a lower-case system name. i.e. sref
    Outputs:
     Returns a list of available hours in the form HH (strings).
    """
    # Loop over items in available runs and add the hour portion for matching
    #  dates and forecast systems.
    return [i[0].split('/')[-1] for i in available_runs if\
             os.path.isdir(i[0]) and i[0].split('/')[-2] == system and\
             i[0].split('/')[-3] == date]
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
        files = glob(GRIB_STORAGE_PATH + '/' + date + '/' + system + '/' +\
                      hour + '/*.grib2')
    elif system == 'gefs':
        files = glob(GRIB_STORAGE_PATH + '/' + date + '/' + system + '/' +\
                      hour + '/*.pgrb2*')
    else:
        raise RuntimeError('Invalid system specified. The system was: %s' %\
                            (system))
    return files
#
if __name__ == '__main__':
    print 'localInventory.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF