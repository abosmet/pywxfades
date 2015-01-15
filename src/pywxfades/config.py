'''
Created on Jan 7, 2015

@author: Joel
'''
# Local package from imports
from manageData import inventory
from plumes import describe
# Standard library from imports
from datetime import datetime
# Standard library imports
import os
import re
#
class Config:
    """
    Class to hold runtime configuration settings.
    Instance Variables:
     model_init_date <string>
       Initialization date of the model in use in the form: YYYYMMDD
     forecast_system <string>
       Lower-case forecast system in use, probably sref or gefs
     model_init_hour <string>
       Initialization hour of the model in use in the form HH
     stations_data_file_name <string>
       File name of the stations data file without path.
     grib_path <string>
       Path to storage directory for the model date and time in use.
     model_fcst_interval <int>
       Time between individual forecasts from the model in use in hours.
     model_fcst_length <int>
       Forecast hour of the final forecast in the model run.
     num_forecasts <int>
       Total number of forecasts in the data set.
     data_types <list>
       Grib shortname of all relevant data to be pulled from grib files. This
        needs to be changed for expansion to other pressure levels.
     model_init_dt <datetime>
       Datetime object representing the initialization time of the model in use.
     indexes <dict>
       Mutable dictionary of indexes for named data (keys). Generated from
        plume descriptions and ModelData and used for accessing data in
        StationData objects.
     test <bool>
       Activate test mode for verbose output in certain situations.
    """
    GRIB_STORAGE_PATH = '../../GRIB'
    STATIONS_DATA_STORAGE_PATH = '../../config'
    OUTPUT_PATH = '../../output'
    DEFAULT_STATIONS_DATA_FILE_NAME = 'paStations.dat'
    TEST_MODE = False
    #
    def __init__(self, params):
        """
        Config may be instantiated without setting any fields. This is designed
         to be configured in stages depending on user input (or lack thereof).
        """
        # Instance variable definitions. These will be assigned later.
        # Basic variables
        self.model_init_date = None
        self.forecast_system = None
        self.model_init_hour = None
        self.stations_data_file_name = None
        # Expanded variables
        self.grib_path = None
        self.model_fcst_interval = None
        self.model_fcst_length = None
        self.num_forecasts = None
        self.model_init_dt = None
        self.indexes = {}
        self.test = Config.TEST_MODE
        return
    #
    def set_default_forecast_system(self):
        """
        Automatically sets the forecast system configuration based on available
         data and the current date setting. This will always prefer SREF data
         over GEFS data if both are available. This will raise a RuntimeError
         if the date configuration was is not set.
        Inputs:
            No physical inputs.
        Outputs:
            No physical outputs. Sets an instance variable.
        """
        # Get available systems from inventory based on instance variable date
        #  and sort reverse alphabetically.
        available_systems = sorted(inventory.get_available_efs_systems(self.model_init_date),reverse=True)
        # SREF will be now be the first element of this list, index 0.
        system = available_systems[0]
        # Set the instance variable.
        self.forecast_system = system
        return
    #
    def set_default_init_date(self):
        """
        Automatically finds the latest available date and sets the date
         configuration. 
        Inputs:
            No physical inputs.
        Outputs:
            No physical outputs. Sets an instance variable.
        """
        # Get available dates from inventory and sort greatest to least.
        available_dates = sorted(inventory.get_available_dates(),reverse=True)
        # The latest date is now the first element (index 0).
        latest_date = available_dates[0]
        # Set the instance variable.
        self.model_init_date = latest_date
        return
    #
    def set_default_init_hour(self):
        """
        Automatically finds the latest available hour based on available data
         and the current date and forecast system settings. This will raise a
         RuntimeError if the date or forecast system configuration is not set.
        """
        # Get available hours from inventory based on current date and forecast
        #  system and sort greatest to least.
        available_hours = sorted(inventory.get_available_hours(self.model_init_date,self.forecast_system),reverse=True)
        # The latest hour is now the first element (index 0).
        latest_hour = available_hours[0]
        # Set the instance variable.
        self.model_init_hour = latest_hour
        return
    #
    def expand(self):
        """
        Expand instance variables which require the basic configuration to be
         set before being created.
        """
        # Check if basic configuration is set.
        if [i for i in [self.model_init_date,self.forecast_system,self.model_init_hour] if i is None]:
            raise RuntimeError('Error expanding configuration. The basic configuration was not set.')
        # Set the grib path using defined init date/time/forecast system.
        # Grib storage paradigm: /GRIB/<date>/<system>/<hour>/*.grib2
        self.grib_path = '%s/%s/%s/%s' % (Config.GRIB_STORAGE_PATH,self.model_init_date,self.forecast_system,self.model_init_hour)
        # Model forecast interval depends on the model in use SREF: 3, GEFS: 6.
        self.model_fcst_interval = 3 if self.forecast_system == 'sref' else 6
        # Model forecast length depends on the model in use SREF: 87, GEFS: 240.
        self.model_fcst_length = 87 if self.forecast_system == 'sref' else 240
        # Number of forecasts in the model run is a function of the forecast
        #  interval and the forecast length.
        self.num_forecasts = (self.model_fcst_length + self.model_fcst_interval) / self.model_fcst_interval
        # Model init time and date can be put into a datetime object. This will
        #  make it easy to create text for graphics and directory structures by
        #  using strftime. Ref: https://docs.python.org/2/library/datetime.html
        self.model_init_dt = datetime.strptime(self.model_init_date + self.model_init_hour,'%Y%m%d%H')
        # Populate some indexes. These will be used to access particular pieces
        #  of data in StationData.
        # TODO: Comments
        plume_count = 0
        for plume in describe.PLUMES:
            self.indexes[plume[0]] = plume_count
            plume_count += 1
            data_count = 0
            for data_type in plume[1]:
                self.indexes[data_type] = data_count
                data_count += 1
        return
    #
    def set_forecast_system(self, system):
        """
        Quality control and set the forecast system configuration.
        Inputs:
            efs_system <String> New forecast system to be set.
        Outputs:
            No physical outputs. Sets an instance variable.
        """
        # Check for a valid forecast system using regular expression.
        if re.search('(?:[sS][rR][eE][fF])|(?:[gG][eE][fF][sS])',system) is not None:
            # Construct the path using the model initialization date.
            system_path = Config.GRIB_STORAGE_PATH + '/' + self.model_init_date
            # Lazy check to see if the directory exists.
            if os.path.exists(system_path) and os.path.isdir(system_path):
                # If it exists and is a directory, set the instance variable.
                self.forecast_system = system.lower()
            else:
                # Stop on directory does not exist.
                raise IOError('Error: The specified directory was not found. The directory was %s' % (system_path))
        else:
            # Stop on invalid forecast system entry.
            raise ValueError('Forecast system not recognized! The system was %s' % (system))
        return
    #
    def set_init_date(self, date):
        """
        Quality control and set the model init date configuration.
        Inputs:
            date <String> New date to be set.
        Outputs:
            No physical outputs. Sets an instance variable.
        """
        # Check for a valid date using regular expression.
        if re.search('\d{8}',date) is not None:
            # Construct path based on input.
            date_path = Config.GRIB_STORAGE_PATH + '/' + date
            # Lazy check to see if the directory exists.
            if os.path.exists(date_path) and os.path.isdir(date_path):
                # If it exists and is a directory, set the instance variable.
                self.model_init_date = date
            else:
                # Stop on directory does not exist.
                raise IOError('Error: The specified directory was not found. The directory was %s' % (date_path))
        else:
            # Stop on invalid date entry.
            raise ValueError('Date not recognized! The date was %s' % (date))
        return
    #
    def set_init_hour(self, hour):
        """
        Quality control and set the model init hour configuration.
        Inputs:
            hour <String> New hour to be set.
        Outputs:
            No physical outputs. Sets an instance variable.
        """
        # Search for valid hours based on forecast system using regular
        #  expression.
        if self.forecast_system == 'sref' and re.search('(?:03)|(?:09)|(?:15)|(?:21)',hour) is not None:
            # Construct path based on input and current date and forecast
            #  system.
            hour_path = Config.GRIB_STORAGE_PATH + '/' + self.model_init_date + '/' + self.forecast_system + '/' + hour
            # Lazy check to see if the directory exists.
            if os.path.exists(hour_path) and os.path.isdir(hour_path):
                # If it exists and is a directory, set the instance variable.
                self.model_init_hour = hour
            else:
                # Stop on directory not found.
                raise IOError('Error: The specified directory was not found. The directory was %s' % (hour_path))
        elif self.forecast_system == 'gefs' and re.search('(?:00)|(?:06)|(?:12)|(?:18)',hour) is not None:
            # Same exact code from the above case, but separated for clarity.
            # Construct path based on input and current date and forecast
            #  system.
            hour_path = Config.GRIB_STORAGE_PATH + '/' + self.model_init_date + '/' + self.forecast_system + '/' + hour
            # Lazy check to see if the directory exists.
            if os.path.exists(hour_path) and os.path.isdir(hour_path):
                # If it exists and is a directory, set the instance variable.
                self.model_init_hour = hour
            else:
                # Stop on directory not found.
                raise IOError('Error: The specified directory was not found. The directory was %s' % (hour_path))
        else:
            # Stop on invalid hour entry.
            raise ValueError('Hour not recognized! The hour was %s' % (hour))
        return
    #
    def set_stations_data_file_name(self, file_name):
        """
        Quality control and set the stations data file name configuration.
        Inputs:
            file_name <String> New file name to be set.
        Outputs:
            No physical outputs. Sets an instance variable.
        """
        # Check for valid file name using regular expression.
        if re.search('(?:.*\.dat)',file_name) is not None:
            # Construct path to specified file.
            file_path = Config.STATIONS_DATA_STORAGE_PATH + '/' + file_name
            # Lazy check to see if file exists.
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # If the file exists and is a file, set the instance variable.
                self.stations_data_file_name = file_name
            else:
                # Stop on file not found.
                raise IOError('Error: The specified file was not found. The file was %s' % (file_path))
        else:
            # Stop on input not recognized or improper file type (extension).
            raise ValueError('Stations Data file name not recognized! The file was %s' % (file_name))
        return
    #
# End Class Config
#
if __name__ == '__main__':
    print 'config.py is not designed to be run as a script.'
    print 'PYTHON STOP'
#
#
#
#
# EOF
