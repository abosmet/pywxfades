'''
Created on Jan 11, 2015

@author: Joel
'''
# Local package imports
import ptype
import thick
import temps
# Begin module code.
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
#  Note: For plumes with data across multiple height levels with the same
#   parameters, please define a separate data request and organize the plotting
#   routine to accommodate. This requirement is to reduce overall memory usage.
#==============================================================================
#
# Define plumes in this list.
PLUMES = [\
          ('Precip-Type', ['tp', 'crain', 'cicep', 'cfrzr', 'csnow'],
           'surface', 0, ptype.plot),
          ('Temp-sfc', ['2t'], 'heightAboveGround', 2, temps.plot),
          ('Temp-850', ['t'], 'isobaricInhPa', 850, temps.plot_null),
          ('Temp-700', ['t'], 'isobaricInhPa', 700, temps.plot_null),
          ('Thick-1k', ['gh'], 'isobaricInhPa', 1000, thick.plot),
          ('Thick-500', ['gh'], 'isobaricInhPa', 500, thick.plot_null)\
]
# End module code.
if __name__ == '__main__':
    print 'describe.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF