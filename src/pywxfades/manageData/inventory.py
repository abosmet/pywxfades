'''
Created on Jan 7, 2015

@author: Joel
'''
# Standard library from imports
from glob import glob
# Standard library imports
import os
# Module constants
GRIB_STORAGE_PATH = '../../../GRIB'
# Begin module code.
# TODO: docstrings
def get_available_dates():
    # Find items living in the grib storage directory and list them.
    raw_glob = glob(GRIB_STORAGE_PATH + '/*')
    # Loop over all items in the grib storage directory and add the name of the
    #  directory without its path if the item is a directory (Linux only!).
    return [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
#
def get_available_efs_systems(date):
    # Find items living in the grib storage directory, date sub-directory.
    raw_glob = glob(GRIB_STORAGE_PATH + '/' + date + '/*')
    # Loop over all items in the date directory and add the name of the
    #  directory without its path if the item is a directory (Linux only!).
    return [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
#
def get_available_hours(date,system):
    # Find items living in the grib storage directory, date sub-directory,
    #  system sub-directory.
    raw_glob = glob(GRIB_STORAGE_PATH + '/' + date + '/' + system + '/*')
    # Loop over all items in the system directory and add the name of the
    #  directory without its path if the item is a directory (Linux only!).
    return [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
#
if __name__ == '__main__':
    print 'inventory.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF