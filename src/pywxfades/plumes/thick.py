'''
Created on Jan 29, 2015

@author: Joel
'''
# Local package imports
import describe
# External library imports
import matplotlib.pyplot as plt
import numpy
# Standard library from imports
from datetime import datetime #@UnusedImport Needed type only.
from datetime import timedelta
# Standard library imports
import os
# Module constants
COLORS = ['#CC0000','#CD2900','#CD5200','#CD7B00','#CDA400','#CDCD00',
          '#A4CD00','#52CD00','#29CD00','#00CD00','#00CD29','#00CD52',
          '#00CD7B','#00CDA4','#00CDCD','#00A4CD','#007BCD','#0052CD',
          '#0029CD','#0000CD','#2900CD','#5200CD','#7B00CD','#A400CD',
          '#CD00CD','#CD00A4','#CD007B','#CD0052','#CD0029','#DA4100']
PRETEXT = '[Thickness]'
# Begin module code.
def plot(sdo, config):
    """
    Plots a plume of 1000-500 mb thickness.
    """
    from stationData import StationData #@UnusedImport @UnresolvedImport
    from modelData import ModelData                   #@UnresolvedImport
    #                                    ^ Need type only,^ Pydev issues
    from config import Config #@UnresolvedImport PyDev issue.
    #
    output_file_path = (Config.OUTPUT_PATH + '/' +
                        config.model_init_dt.strftime('%Y%m%d/%HZ') + '/' +
                        'Thickness' + '/' + str(sdo.station_name) + '.png')
    # Grab relevant data.
    H50_ht = sdo.data[config.indexes[describe.PLUMES[7][0]]]
    H70_ht = sdo.data[config.indexes[describe.PLUMES[6][0]]]
    H85_ht = sdo.data[config.indexes[describe.PLUMES[5][0]]]
    H100_ht = sdo.data[config.indexes[describe.PLUMES[4][0]]]
    # Plot the member color key.
    plt.axes([0.0, 0.0, 0.2, 1.0], frameon=False, axisbg='w')
    plt.xticks([]), plt.yticks([])
    plt.text(0.050, 1 - 0.033, 'Color Key', ha='left', size=10, color='#8200dc')
    for mdl in ModelData.member_names:
        plt.text(0.050, 1 - ((config.indexes[mdl] + 2) * 0.033), mdl,
                 ha='left', size=10, color=COLORS[config.indexes[mdl]])
    # Define an axis for the 1000-500 mb thickness plot.
    plt.axes([0.2000, 0.5250, 0.7500, 0.3750])
    # Define x-axis text labels based on forecast initialization time.
    label_num = 0
    labels = []
    # Loop over all times create a label based on forecast time and conditions.
    for i in range(0, H50_ht.shape[2]):
        # Start at model init date/time, each step add time between forecasts.
        now = config.model_init_dt +\
                timedelta(hours=(i * config.model_fcst_interval))
        # Plot text every 24 for GEFS, every 12 hours for SREF, starting 0Z.
        # Year to be printed on first appearing label.
        # Date to be printed on all 0Z labels.
        # Empty string to be printed on all other labels.
        if (now.hour == 0 or
                (now.hour == 12 and config.forecast_system == 'sref')):
            label_num += 1
            if label_num == 1:
                label = now.strftime('%HZ\n%d%b\n%Y').upper()
            elif now.hour == 0:
                label = now.strftime('%HZ\n%d%b').upper()
            else:
                label = now.strftime('%HZ').upper()
        else:
            label = ''
        # Add string to list of labels.
        labels.append(label)
    # Transform label list into an array.
    labels = numpy.array(labels)
    # Draw the true plot.
    # Loop over all models.
    for mdl in range(0, H50_ht.shape[1]):
        H50_data = H50_ht[config.indexes['gh']][mdl]
        H100_data = H100_ht[config.indexes['gh']][mdl]
        line_data = (H50_data - H100_data) / 10 # Thickness in decameters
        mean = numpy.mean(line_data)
        sd = numpy.std(line_data)
        # QC values for extremes.
        for i in range(0,line_data.shape[0]):
            if line_data[i] < mean - 3 * sd or line_data[i] > mean + 3 * sd:
                line_data[i] = numpy.nan
        plt.plot(line_data,COLORS[mdl],lw=0.50,
                 marker='o',markersize=2)
    # Set the x-axis of the plot. (where,what,size in points).
    plt.xticks(numpy.arange(0, H50_ht.shape[2]),[],size=10)
    # Find the range of the y-axis.
    y_max = numpy.max(plt.yticks()[0])
    y_min = numpy.min(plt.yticks()[0])
    # Draw a critical point line if the y-axis limits permit.
    if 540 < y_max and 540 > y_min:
        plt.plot([0,H50_ht.shape[2] - 1],[540,540],color='r',lw=1)
    # Set the y-axis label.
    plt.ylabel(u'1000-500mb (dam)', color='#8200dc', size=12)
    # Define an axis for the 850-700 mb thickness plot.
    plt.axes([0.2000, 0.3375, 0.7500, 0.1875])
    # Draw the true plot.
    # Loop over all models.
    for mdl in range(0, H85_ht.shape[1]):
        H85_data = H85_ht[config.indexes['gh']][mdl]
        H70_data = H70_ht[config.indexes['gh']][mdl]
        line_data = (H70_data - H85_data) / 10 # Thickness in decameters
        mean = numpy.mean(line_data)
        sd = numpy.std(line_data)
        # QC values for extremes.
        for i in range(0,line_data.shape[0]):
            if line_data[i] < mean - 3 * sd or line_data[i] > mean + 3 * sd:
                line_data[i] = numpy.nan
        plt.plot(line_data,COLORS[mdl],lw=0.50,
                 marker='o',markersize=2)
    # Set the x-axis of the plot. (where,what,size in points).
    plt.xticks(numpy.arange(0, H85_ht.shape[2]),[],size=10)
    # Find the range of the y-axis.
    y_max = numpy.max(plt.yticks()[0])
    y_min = numpy.min(plt.yticks()[0])
    # Draw a critical point line if the y-axis limits permit.
    if 154 < y_max and 154 > y_min:
        plt.plot([0,H85_ht.shape[2] - 1],[154,154],color='r',lw=1)
    # Set a reasonable number of y-axis ticks.
    step = int(round((y_max - y_min) / 5.0))
    plt.yticks(numpy.arange(y_min, y_max, step), size=10)
    # Set the y-axis label.
    plt.ylabel(u'850-700mb', color='#8200dc', size=12)
    # Define axis for the 1000-850mb thickness plot.
    plt.axes([0.2000, 0.1500, 0.7500, 0.1875])
    # Draw the true plot.
    # Loop over all models.
    for mdl in range(0, H85_ht.shape[1]):
        H85_data = H85_ht[config.indexes['gh']][mdl]
        H100_data = H100_ht[config.indexes['gh']][mdl]
        line_data = (H85_data - H100_data) / 10 # Thickness in decameters
        mean = numpy.mean(line_data)
        sd = numpy.std(line_data)
        # QC values for extremes.
        for i in range(0,line_data.shape[0]):
            if line_data[i] < mean - 3 * sd or line_data[i] > mean + 3 * sd:
                line_data[i] = numpy.nan
        plt.plot(line_data,COLORS[mdl],lw=0.50,
                 marker='o',markersize=2)
    # Set the x-axis of the plot. (where,what,size in points).
    plt.xticks(numpy.arange(0, H85_ht.shape[2]),labels,size=10)
    # Find the range of the y-axis.
    y_max = numpy.max(plt.yticks()[0])
    y_min = numpy.min(plt.yticks()[0])
    # Draw a critical point line if the y-axis limits permit.
    if 130 < y_max and 130 > y_min:
        plt.plot([0,H85_ht.shape[2] - 1],[130,130],color='r',lw=1)
    # Set a reasonable number of y-axis ticks.
    step = int(round((y_max - y_min) / 5.0))
    plt.yticks(numpy.arange(y_min, y_max, step), size=10)
    # Set the y-axis label.
    plt.ylabel(u'1000-850mb', color='#8200dc', size=12)
    # Plot the title panel.
    plt.axes([0.25, 0.9, 0.7, 0.1], frameon=False, axisbg='w')
    plt.xticks([]), plt.yticks([])
    plot_title = '%s Ensemble Member Forecast Initialized %s\nInstantaneous %s'\
                 ' Hourly Thickness (dam) coded by EFS\nColors represent '\
                 'individual member models.' % \
                 (config.forecast_system.upper(),
                  config.model_init_dt.strftime('%HZ%d%b%Y').upper(),
                  config.model_fcst_interval)
    plt.text(0.5,0.5,plot_title,ha='center',va='center',size=10,color='#8200dc')
    # Plot the station information panel.
    plt.axes([0.25, 0.05, 0.65, 0.1], frameon=False, axisbg='w')
    plt.xticks([]),plt.yticks([])
    # Generate text based on station.
    station_text = 'Station Data Plot for: %s Coords: %02.02f %02.02f\nNearest'\
                   ' Point Coords: %02.02f %02.02f, Distance: %02.02f km' %\
                   (sdo.station_name, sdo.latitude, sdo.longitude, sdo.grib_lat,
                     sdo.grib_lon, sdo.get_dist_to_nearest_grid_point())
    plt.text(0.6, 0.15, station_text, ha='center', va='center', size=10,
             color='#8200dc')
    # Create output directories if they don't exist.
    cur_output_path = '/'.join(output_file_path.split('/')[:-1])
    if not os.path.exists(cur_output_path):
        os.makedirs(cur_output_path)
    # Save the figure.
    plt.savefig(output_file_path)
    plt.clf()
    return
#
def plot_null(*args):
    pass
#
if __name__ == '__main__':
    print 'thick.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF