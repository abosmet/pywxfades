'''
Created on Jan 10, 2015

@author: Joel
'''
#
from pywxfades.modelData import ModelData
#
class StationData:
    """
    This class will manage data and static information about each station.
    Data storage will be created once it is needed. Storage will be in the form
     of multi-tiered numpy arrays.
    Instance Variables:
     latitude <float>
      Latitude of the station in degrees, range: [-90,90]
     longitude <float>
      Longitude of the station in degrees, range: [-180,180]
     station_name <string>
      Name of the station, i.e. Scranton,PA
     grib_i <int>
      x-coordinate reference from grib lat/lon grid used for accessing data 
       from grib messages.
     grib_j <int>
      y-coordinate reference from grib lat/lon grid used for accessing data 
       from grib messages.
     grib_lat <float>
      Latitude of the nearest grid point from the model.
     grib_lon <float>
      Longitude of the nearest grid point from the model.
     model_member_indexes <dict>
      Dictionary by member name of access index for data organization.
    """
    # Instances of this class will be added to a list for later iteration.
    instances = []
    #
    def __init__(self,lat,lon,name):
        """
        Instantiate the StationData object with the given latitude and
         longitude. Grib coordinates and access indexes will be set when the
         first grib file is opened.
        """
        self.latitude = lat
        self.longitude = lon
        self.station_name = name
        self.grib_i = None
        self.grib_j = None
        self.grib_lat = None
        self.grib_lon = None
        # Define a dictionary to keep track of models in the data for this
        #  station. Dictionary comprehension.
        self.model_member_indexes = {ModelData.member_names[i] : i for i in range(0,len(ModelData.member_names))}
        # Add this object to the list of StationData objects.
        StationData.instances.append(self)
    #
# End Class StationData
#
if __name__ == '__main__':
    print 'stationData.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF