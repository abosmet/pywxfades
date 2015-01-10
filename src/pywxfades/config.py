'''
Created on Jan 7, 2015

@author: Joel
'''
#
from pywxfades.manageData import inventory
#
import os
import re
#
class Config:
    """
    Class to hold runtime configuration settings.
    """
    GRIB_STORAGE_PATH = '../../GRIB'
    STATIONS_DATA_STORAGE_PATH = '../../config'
    DEFAULT_STATIONS_DATA_FILE_NAME = 'paStations.dat'
    #
    def __init__(self, params):
        """
        Config may be instantiated without setting any fields. This is designed
         to be configured in stages depending on user input (or lack thereof).
        """
        self.model_init_date = None
        self.forecast_system = None
        self.model_init_hour = None
        self.stations_data_file_name = None
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
        available_hours = sorted(inventory.get_available_dates(),reverse=True)
        # The latest hour is now the first element (index 0).
        latest_hour = available_hours[0]
        # Set the instance variable.
        self.model_init_hour = latest_hour
        return
    #
    def expand(self):
        pass
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
