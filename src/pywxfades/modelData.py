'''
Created on Jan 10, 2015

@author: Joel
'''
class ModelData:
    """
    This class will keep track of and manipulate model data files.
    Instance Variables:
     grib_file_path <string>
      Path to the grib file this object represents.
     member_name <string>
      Name of the member model from which this file comes.
    """
    member_names = []
    instances = []
    #
    def __init__(self,grib):
        """
        Instantiate the ModelData object.
        """
        self.grib_file_path = grib
        self.member_name = ModelData.get_member_name_from_path(grib)
        if self.member_name not in ModelData.member_names:
            ModelData.member_names.append(self.member_name)
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