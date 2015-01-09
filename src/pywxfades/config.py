'''
Created on Jan 7, 2015

@author: Joel
'''

class Config:
    """
    Class to hold runtime configuration settings.
    """
    GRIB_STORAGE_PATH = '../../GRIB'
    STATIONS_DATA_STORAGE_PATH = '../../config'
    DEFAULT_STATIONS_DATA_FILE_NAME = 'paStations.dat'
    #
    def __init__(self,params):
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
    def set_init_date(self,params):
        pass
    #
    def set_default_init_date(self):
        pass
    #
    def set_forecast_system(self,params):
        pass
    #
    def set_default_forecast_system(self):
        pass
    #
    def set_init_hour(self,params):
        pass
    #
    def set_default_init_hour(self):
        pass
    #
    def set_stations_data_file_name(self,params):
        pass
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