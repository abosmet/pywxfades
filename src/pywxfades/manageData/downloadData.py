'''
Created on Jan 20, 2015

@author: Joel
'''
# Standard library from imports
from datetime import datetime
from datetime import timedelta #@UnusedImport Need type only.
from ftplib import FTP
# Standard library imports
import os
import re
import socket
import time
# Module constants
GRIB_STORAGE_PATH = '../../GRIB'
NCEP_FTP_SERVER = 'ftpprd.ncep.noaa.gov'
NCEP_GEFS_DIR = 'pub/data/nccf/com/gens/prod/gefs.'
NCEP_SREF_DIR = 'pub/data/nccf/com/sref/prod/sref.'
PRETEXT = '[downloadData]'
# Begin module code.
def download_spec(date,system,hour):
    """
    Build local and remote paths from specifications and download data.
    Inputs:
        date <string>
         String representing the desired model initialization date, in the form
          YYYYMMDD.
        system <string>
         Ensemble forecast system name in lower-case letters, i.e. sref
        hour <string>
         String representing the desired model initialization time, in the form
          HH.
    Outputs:
        No physical outputs. Calls a subroutine which will write files to disk.
    """
    local_path = '{0}/{1}/{2}/{3}'.format(GRIB_STORAGE_PATH, date, system, hour)
    if system == 'gefs':
        remote_path = '{0}{1}/{2}/pgrb2a'.format(NCEP_GEFS_DIR, date, hour)
    elif system == 'sref':
        remote_path = '{0}{1}/{2}/pgrb'.format(NCEP_SREF_DIR, date, hour)
    else:
        raise RuntimeError('Invalid forecast system in download specification!'\
                           ' The system was: %s' % (system))
    download(local_path,remote_path)
    return
#
def download(local_path,remote_path):
    """
    Download data from the NCEP servers.
    Inputs:
        local_path <string>
         Path to a folder where the grib files should be stored after download.
        remote_path <string>
         Path to a folder where the grib files are stored on the NCEP server.
    Outputs:
        No physical outputs. Calls a subroutine which will write files to disk.
    """
    # Create local storage directories if they do not exist.
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    # Define an FTP object and log into the NCEP server.
    ftp = FTP(NCEP_FTP_SERVER)
    ftp.login()
    # Pull the forecast system from the remote file path.
    system = remote_path.split('/')[-3].split('.')[0]
    # Define file pattern based on forecast system.
    if system == 'gefs':
        remote_file_list = ftp.nlst('{0}/*.pgrb2af*'.format(remote_path))
    elif system == 'sref':
        remote_file_list = ftp.nlst('{0}/*.grib2'.format(remote_path))
    else:
        raise RuntimeError('Invalid forecast system in download specification!'\
                           ' The system was: %s' % (system))
    # Filter the file list to download the correct data files.
    download_list = filter_file_list(remote_file_list,system)
    # Loop over files in download list and download them if they aren't present
    #  on the local file system.
    for remote_file_path in download_list:
        # Copy the file name to the local path.
        local_file_path = '{0}/{1}'.format(local_path,
                                           remote_file_path.split('/')[-1])
        # Do not download if the file exists locally.
        if os.path.exists(local_file_path) and os.path.isfile(local_file_path):
            print '%s File %s/%s exists locally, skipping file:\n\t%s' %\
                    (PRETEXT, download_list.index(remote_file_path) + 1,
                     len(download_list), local_file_path)
        else:
            print '%s File download %s/%s in progress. . .\nRemote File: %s\n '\
            '>> Local File: %s' % (PRETEXT,
                                   download_list.index(remote_file_path) + 1,
                                   len(download_list), remote_file_path,
                                   local_file_path)
            retrieve_file(ftp, remote_file_path, local_file_path)
    # Close the FTP object before returning.
    ftp.close()
    pass
#
def filter_file_list(file_list,system):
    """
    Return a list of files to download by filtering a list of files.
    Inputs:
        file_list <list>
         List of files (including paths) which are candidates to be downloaded
          from the NCEP server.
        system <string>
         Ensemble forecast system name in lower-case letters, i.e. sref
    Outputs:
        valid_file_list <list>
         List of files which should be downloaded.
    """
    # Define valid file list to be built recursively.
    valid_file_list = []
    # Define regular expression based on forecast system.
    if system == 'gefs':
        regex = 'ge[cp]\d{2}\.t\d{2}z\.pgrb2af(\d{2,3})$'
    elif system == 'sref':
        regex = 'sref_\w{2,3}\.t\d{2}z\.pgrb132.\w{2,3}\.grib2$'
    else:
        raise RuntimeError('Invalid forecast system in download specification!'\
                           ' The system was: %s' % (system))
    # Loop over all available files and filter using the regex.
    for file_ in file_list:
        match = re.search(regex,file_)
        if match is not None:
            if system == 'gefs' and int(match.groups(1)[0]) <= 240:
                valid_file_list.append(file_)
            elif system == 'sref':
                valid_file_list.append(file_)
            else:
                pass
    return valid_file_list
#
def retrieve_file(ftp_handle,remote_file,local_file):
    """
    Download a file from the ftp handle a store it in the specified local file.
    Inputs:
        ftp_handle <FTP>
         FTP object opened and connected to the NCEP server.
        remote_file <string>
         Name, including path, of the file to download on the NCEP server.
        local_file <string>
         Name, including path, of the file to in which to store the download.
    Outputs:
        No physical outputs. Writes a file to disk.
    """
    # Open the local file in binary write mode.
    local_file_handle = open(local_file,'wb')
    # Record the time before the request to the server was made. This prevents
    #  the program from spamming the server with tons of requests.
    time_before_request = datetime.now()
    # Keep trying until the download succeeds or exceeding 10 attempts.
    keep_going = True
    timeout_count = 0
    while keep_going:
        # Try/except for timeout errors.
        try:
            ftp_handle.retrbinary('RETR ' + remote_file,
                                  local_file_handle.write)
            keep_going = False
        except socket.error:
            # Wait for a bit on after a timeout.
            time.sleep(3)
            timeout_count += 1
            if timeout_count > 10:
                # Cleanup the file if too many timeouts occurred.
                local_file_handle.close()
                os.remove(local_file)
                keep_going = False
                raise RuntimeError('Exceeded timeout limit. Program will termi'\
                                   'nate.')
            else:
                print '%s Connection timed out, retrying. . . Attempt %s of 10'\
                        % (PRETEXT, timeout_count)
    # Pause for a bit if the download didn't take long.
    if (datetime.now() - time_before_request).seconds < 5:
        time.sleep(2)
    # Close the open file.
    local_file_handle.close()
    return
#
if __name__ == '__main__':
    print 'downloadData.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF