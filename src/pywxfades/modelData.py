'''
Created on Jan 10, 2015

@author: Joel
'''
#
from plumes import describe
#
#from stationData import StationData
#
import pygrib #@UnresolvedImport pygrib not available on windows.
#
class ModelData:
    """
    This class will keep track of and manipulate model data files.
    Instance Variables:
     grib_file_path <string>
      Path to the grib file this object represents.
     member_name <string>
      Name of the member model from which this file comes.
     config <Config>
      Config object holding runtime configuration.
    """
    member_names = []
    instances = []
    #
    def __init__(self,grib,config):
        """
        Instantiate the ModelData object.
        """
        self.grib_file_path = grib
        self.member_name = ModelData.get_member_name_from_path(grib)
        if self.member_name not in ModelData.member_names:
            ModelData.member_names.append(self.member_name)
        self.config = config
        ModelData.instances.append(self)
        return
    #
    @staticmethod
    def get_member_name_from_path(path):
        """
        Pulls the member name from a grib file's path.
        The process is different depending on the model.
        ../../GRIB/20140228/sref/15/sref_em.t15z.pgrb212.n3.grib2
                ''/Date/System/Hour/MemberName.???.???
        ../../GRIB/20140228/gefs/12/gespr.t06z.pgrb2af90
                ''/Date/System/Hour/MemberName.???.???
        Inputs:
         path <string>
          Path to a grib file.
        Outputs:
         Returns the member name (string).
        """
        # Get the system name from the file's path (index 4 of a split on /).
        split_path = path.split('/')
        system = split_path[4]
        file_name = split_path[-1]
        split_file_name = file_name.split('.')
        if system == 'sref':
            member_name = split_file_name[0] + '-' + split_file_name[3]
        elif system == 'gefs':
            member_name = split_file_name[0]
        else:
            raise RuntimeError('Invalid forecast system! The system was: %s' % (system))
        return member_name
    #
    def populate_data(self):
        """
        Open the grib file and read data. Alerts all StationData objects of
         all grib messages, creating grib i j data if necessary. This reads a
         list of plume data requirements and dynamically pulls and sends data.
        Inputs:
            No physical inputs.
            Requires StationData objects be initialized.
        Outputs:
            No physical outputs.
            Enters data into StationData objects.
        """
        # Importing StationData with the standard imports causes a redundancy
        #  problem, so it is imported here only when it is needed.
        from stationData import StationData
        # Find data requirements from all plumes.
        requirements = describe.PLUMES
        # Loop over plumes and define parameters to be used for pulling data.
        grib_file = pygrib.open(self.grib_file_path)
        for req in requirements:
            (plume,data_types,grid_level_type,grid_level,unused) = req
            selected = grib_file.select(shortName=data_types,typeOfLevel=grid_level_type,level=grid_level)
            for message in selected:
                for sdo in StationData.instances:
                    if sdo.grib_i is None:
                        StationData.populate_grid_information(message,self.config)
                    sdo.add_data(plume,self.member_name,message)
        grib_file.close()
        return
    #
# End Class ModelData
#
if __name__ == '__main__':
    print 'modelData.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF