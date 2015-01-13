'''
Created on Jan 11, 2015

@author: Joel
'''
#
import ptype
#
#==============================================================================
# List plume configurations here.
# (Plume name,shortName,typeOfLevel,level,plot method)
#  Plume Name: <string>
#   Text name for the type of plume. This has no functional value, but could be
#    used to create debug text.
#  shortName: <list>
#   List of grib shortName values to be used to pulling grib data. The pygrib
#    select method may be used with a list of shortNames to pull all of them so
#    long as they all have the same typeOfLevel and level. This list will also
#    be used to reference data in memory during processing.
#  typeOfLevel: <string>
#   Grib typeOfLevel to be used for the plot. This is necessary to select data.
#    Possible typeOfLevel values: surface isobaricInhPa
#  level: <int> or <string>
#   Grib level to be used for the plot. This is necessary to select data.
#    ptype plumes use a level of 0
#  plot method: <function>
#   Function to be used to plot the plume. Can be called with tuple[4](args)
#==============================================================================
PLUMES = [('Precip-Type', ['tp', 'crain', 'cicep', 'cfrzr', 'csnow'], 'surface', 0, ptype.plot)\
                                      ]
#
if __name__ == '__main__':
    print 'describe.py is not designed to be run independently.'
    print 'PYTHON STOP'
