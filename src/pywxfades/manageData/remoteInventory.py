'''
Created on Jan 19, 2015

@author: Joel
'''
# Standard library from imports
from ftplib import FTP
# Standard library imports
import os
# Module constants
LOCAL_GRIB_PATH = '../../GRIB'
NCEP_FTP_SERVER = 'ftpprd.ncep.noaa.gov'
NCEP_SREF_DIR = 'pub/data/nccf/com/sref/prod/sref.*'
NCEP_GEFS_DIR = 'pub/data/nccf/com/gens/prod/gefs.*'
NCEP_SREF_REF_TOTAL = 5082
NCEP_GEFS_REF_TOTAL = 3032
PRETEXT = '[remoteInventory]'
# Available runs to be populated on package import if remote runs are to be
#  included.
available_runs = []
# Begin module code.
def gen_available_runs():
    """
    Uses FTP NLST commands to find available model runs on the NCEP servers.
    Inputs:
        No physical inputs.
    Outputs:
        No physical outputs. Sets a module-level variable.
    """
    ftp = FTP(NCEP_FTP_SERVER)
    ftp.login()
    run_dirs = []
    # Scan for SREF model runs.
    print '%s Scanning remote file inventory. This may take a while.' %\
        (PRETEXT)
    for date_dir in ftp.nlst(NCEP_SREF_DIR):
        for hour_dir in ftp.nlst('{0}/*'.format(date_dir)):
            if len(ftp.nlst('{0}/pgrb'.format(hour_dir))) ==\
                NCEP_SREF_REF_TOTAL:
                run_dirs.append(hour_dir)
    # Scan for GEFS model runs.
    for date_dir in ftp.nlst(NCEP_GEFS_DIR):
        for hour_dir in ftp.nlst('{0}/*'.format(date_dir)):
            if len(ftp.nlst('{0}/pgrb2a'.format(hour_dir))) ==\
                NCEP_GEFS_REF_TOTAL:
                run_dirs.append(hour_dir)
    # Close the FTP connection as it is no longer needed.
    ftp.close()
    # Construct tuples with information about each run. Identical functionality
    #  to localInventory.
    print '%s Generating remote run inventory.' % (PRETEXT)
    for folder in run_dirs:
        split_path = folder.split('/')
        hour_str = split_path[-1]
        date_str = split_path[-2].split('.')[1]
        system = split_path[-2].split('.')[0]
        # Construct the local path for this data
        local_path = '{0}/{1}/{2}/{3}'.format(LOCAL_GRIB_PATH, date_str, system,
                                              hour_str)
        # Construct a description to be used for UI selections.
        desc = '{0}-{2}-{4}\t{3}Z\t{1}\tREMOTE'.format(date_str[0:4], system,
                                                       date_str[4:6], hour_str,
                                                       date_str[6:8])
        # Create the tuple and add to the list of available runs.
        run = (local_path, desc)
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
if __name__ == '__main__':
    print 'remoteInventory.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF