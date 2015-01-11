#!/usr/bin/python
'''
Created on Jan 7, 2015

@author: Joel
'''
# Local package imports
from pywxfades.config import Config
from pywxfades.manageData import inventory
from pywxfades.modelData import ModelData
from pywxfades.stationData import StationData
from pywxfades import ui
# Standard library imports
import sys
# Begin module code
def gen_model_data_objects(config):
    """
    Creates ModelData objects from a list of grib files.
    """
    files = inventory.get_data_file_list(config.model_init_date,config.forecast_system,config.model_init_hour)
    for file_ in files:
        ModelData(file_)
    return
#
def gen_station_data_objects(config):
    """
    Reads the stations data file and creates StationData objects for all
     listed stations. Stations data file is formatted as the following:
     <latitude> <longitude> <station name>\n
    """
    # Open the stations data file for the duration of this task.
    with open(Config.STATIONS_DATA_STORAGE_PATH + '/' + config.stations_data_file_name,'r') as f:
        # Loop over all lines in the stations data file.
        for lines in f:
            # Remove newline and EOF sigils.
            line = lines.strip('\n\r')
            # Split on whitespace and set local variables.
            (lat,lon,name) = line.split()
            # Create a StationData object.
            StationData(float(lat),float(lon),name)
            if config.test:
                print 'New station created! Name: %s Lat: %s Lon: %s' % (name,lat,lon)
    return
#
def main():
    """
    Entry point of program.
    """
    PRETEXT = '[Plumes]'
    print '%s Initializing. . .' % (PRETEXT)
    # Define a configuration object.
    config = Config('')
    # Check for command line arguments, if found, parse them. At least 1
    #  argument must have been entered, the name of this file.
    # This if statement will pass control flow to a subcommand and allow the
    #  subcommand to determine how to continue. Upon exiting the if block, this
    #  process assumes that config is set and continues.
    parse_arguments(config)
    # Expand the configuration.
    config.expand()
    # Create ModelData objects.
    gen_model_data_objects(config)
    # Create StationData objects.
    gen_station_data_objects(config)
    # TODO: To Be Continued...
    return
#
def parse_arguments(config):
    """
    Abstracted from main() as this is one complete thought.
    Reads and processes command line arguments.
    Should be able to process the following:
    -Date in the form YYYYMMDD, probably delimited by -d or -D
    -Hour in the form HH, probably delimited by a -h or -H
    -Model system, either GEFS or SREF, probably delimited by -m/-M
      This could also accept gefs or sref, lowercase versions.
    -A stations data file to use, probably delimited by -s or -S
      This will allow for manual running for research graphics.
      This could be extended for other systems as well, such as SREFPARA, 
      NAEFSBC, etc.
    -Help in the form help, ?, /?, -help, -HELP. This should print out syntax
      and command line arguments for the user to use.
    -UI in the form -ui or -UI. This will present the user with menus to pick
      an available date, time, model, station data file and graphic type.
    """
    #==========================================================================
    # When the user inputs dates, times, etc on the command line, the program
    #  should make sure that those items are available in the data inventory.
    #  The program should terminate if the selections are unavailable.
    # First, the program will check for any help or UI requests, because those
    #  will bypass the normal command-line arguments.
    # If help or a UI were not requested, the program will parse command line
    #  arguments. If no arguments are set at all, it will default to loading
    #  the latest available data, preferring SREF data when SREF and GEFS are
    #  both available.
    # If some arguments are left out, the program will attempt to dynamically
    #  define missing arguments. If, however, the user inputs are not valid for
    #  dynamically defined values, the program will terminate. User inputs are
    #  paramount.
    #==========================================================================
    #
    # Check supplied arguments for help delimiters.
    if ([i for i in ['help','-help','/help','-HELP','/HELP','?','-?','/?'] if i in sys.argv]):
        print_help()
        print 'PYTHON STOP'
        exit()
    # Check supplied arguments for UI request.
    elif ([i for i in ['-ui','-UI'] if i in sys.argv]):
        user_interface(config)
    # Otherwise, check for setting delimiters.
    else:
        #======================================================================
        # List comprehensions to define arg_index. This will add the index of
        #  the matching argument to a list. In the event of multiple occurrences
        #  of the same argument, indexes will appear for all matches. As a
        #  matter of convention, this program will always use the first
        #  occurrence so as to eliminate confusion and problems.
        # This will occur for each possible argument type.
        # Setter functions are not standard python, but in this case they are
        #  necessary in order to perform the required quality control.
        #======================================================================
        #
        # Date argument check.
        arg_index = [(sys.argv.index(i) + 1) for i in ['-d','-D'] if i in sys.argv]
        if arg_index:
            # If this argument is set, the next argument should be a date.
            # config.set_init_date() will check for validity.
            arg_init_date = sys.argv[arg_index[0]]
            config.set_init_date(arg_init_date)
        else:
            config.set_default_init_date()
        # Forecast system argument check.
        arg_index = [(sys.argv.index(i) + 1) for i in ['-m','-M'] if i in sys.argv]
        if arg_index:
            # If this argument is set, the next argument should be a forecast
            #  system. config.set_forecast_system() will check for validity.
            arg_forecast_system = sys.argv[arg_index[0]]
            config.set_forecast_system(arg_forecast_system)
        else:
            config.set_default_forecast_system()
        # Hour argument check.
        arg_index = [(sys.argv.index(i) + 1) for i in ['-h','-H'] if i in sys.argv]
        if arg_index:
            # If this argument is set, the next argument should be a hour.
            #  config.set_init_hour() will check for validity.
            arg_init_hour = sys.argv[arg_index[0]]
            config.set_init_hour(arg_init_hour)
        else:
            config.set_default_init_hour()
        # Stations data file argument check.
        arg_index = [(sys.argv.index(i) + 1) for i in ['-s','-S'] if i in sys.argv]
        if arg_index:
            # If this argument is set, the next argument should be a stations
            #  data file. This must be a .dat file and must exist.
            #  config.set_stations_data_file() will check for validity.
            arg_stations_data_file_name = sys.argv[arg_index[0]]
            config.set_stations_data_file(arg_stations_data_file_name)
        else:
            config.set_stations_data_file(Config.DEFAULT_STATIONS_DATA_FILE_NAME)
    return
#
def print_help():
    """
    Prints the help dialogue to the terminal.
    """
    print '[Plumes]'
    print 'Syntax:'
    print '\t./main.py [option] [argument] ...'
    print 'Description:'
    print '\tThis program produces the following plume diagrams:'
    print '\tPrecipitation Type'
    print 'Options:'
    print '\t-d, -D [argument]'
    print '\t\tSpecify a date in the format YYYYMMDD\n'
    print '\t-h, -H [argument]'
    print '\t\tSpecify a hour as a zero-padded integer, HH\n'
    print '\t-m, -M [argument]'
    print '\t\tSpecify a model, either SREF or GEFS\n'
    print '\t-s, -S [argument]'
    print '\t\tSpecify a stations data file, *.dat\n'
    print '\t-?, -help, -HELP'
    print '\t\tDisplay this dialogue.\n'
    print '\t-ui, -UI'
    print '\t\tRequest a user interface to make selections'
    print '\t\tfrom available data.'
    return
#
def user_interface(config):
    """
    This function will produce a user interface allowing selections to be made.
    A huge amount of code will be going in here and possibly an entire package.
    This will make use of several data inventory functions.
    """
    ui.show(config)
    return
#
if __name__ == '__main__':
    main()
    print 'PYTHON STOP'
#
#
#
#
# EOF