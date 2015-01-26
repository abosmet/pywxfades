'''
Created on Jan 21, 2015

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
COLORSV1=['#DA3F21','#DA5E21','#DA7D21','#DA9C21','#DABB21','#DADA21',
          '#BBDA21','#9CDA21','#21DABB','#21DADA','#21BBDA','#219CDA',
          '#217DDA','#215EDA','#213FDA','#2121DA','#3F21DA','#5E21DA',
          '#7D21DA','#9C21DA','#BB21DA','#DA21DA','#DA21BB','#DA219C',
          '#DA217D','#DA215E','#DA213F','#DA2121','#FF0000','#FF0040']
COLORS = ['#CC0000','#CD2900','#CD5200','#CD7B00','#CDA400','#CDCD00',
          '#A4CD00','#52CD00','#29CD00','#00CD00','#00CD29','#00CD52',
          '#00CD7B','#00CDA4','#00CDCD','#00A4CD','#007BCD','#0052CD',
          '#0029CD','#0000CD','#2900CD','#5200CD','#7B00CD','#A400CD',
          '#CD00CD','#CD00A4','#CD007B','#CD0052','#CD0029','#DA4100']
PRETEXT = '[Temps]'
# Begin module code.
def plot(sdo,config):
    """
    Plots a plume of precipitation data for the surface, 850 mb and 700 mb.
    Process:
     Pull in data, plot a line for each model on each panel.
    """
    from stationData import StationData #@UnusedImport @UnresolvedImport
    #                                    ^ Need type only,^ Pydev issues
    from config import Config #@UnresolvedImport PyDev issue.
    output_file_path = (Config.OUTPUT_PATH + '/' +
                        config.model_init_dt.strftime('%Y%m%d/%HZ') + '/' +
                        'Temperatures' + '-' + str(sdo.station_name) +
                        '.png')
    # Grab relevant data.
    sfc_data = sdo.data[config.indexes[describe.PLUMES[1][0]]] # COMPLEX
    h85_data = sdo.data[config.indexes[describe.PLUMES[2][0]]]
    h70_data = sdo.data[config.indexes[describe.PLUMES[3][0]]]
    # Define axis for surface temperatures.
    plt.axes([0.1500, 0.5250, 0.8000, 0.3750])
    # Define x-axis text labels based on forecast initialization time.
    label_num = 0
    labels = []
    # Loop over all times create a label based on forecast time and conditions.
    for i in range(0,sfc_data.shape[2]):
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
    # Set the x-axis of the plot. (where,what,size in points).
    plt.xticks(numpy.arange(0, sfc_data.shape[2]),labels,size=10)
    # Draw the true plot.
    # Loop over all models (shape[1]).
    for mdl in range(0,sfc_data.shape[1]):
        line_data = sfc_data[config.indexes['2t']][mdl]
        mean = numpy.mean(line_data)
        sd = numpy.std(line_data)
        # QC values for extremes.
        for i in range(0,line_data.shape[0]):
            if line_data[i] < mean - 3 * sd or line_data[i] > mean + 3 * sd:
                line_data[i] = numpy.nan
        line_data_deg_f = (line_data - 273.15) * (9.0/5.0) + 32
        plt.plot(line_data_deg_f,COLORS[mdl],lw=0.50,
                 marker='o',markersize=2)
    # Plot the freezing point line. TODO: Check if this is within the y-axis limits.
    plt.plot([0,sfc_data.shape[2] - 1],[32,32],color='r',lw=1)
    # Set the y-axis label.
    plt.ylabel(u'Surface (\u00b0F)')
    # Define axis for 850 mb temperatures.
    plt.axes([0.1500, 0.3375, 0.8000, 0.1875])
    # Set the x-axis of the plot. (where,what,size in points).
    plt.xticks(numpy.arange(0, sfc_data.shape[2]),labels,size=10)
    # Draw the true plot.
    # Loop over all models (shape[1]).
    for mdl in range(0,sfc_data.shape[1]):
        line_data = h85_data[config.indexes['t']][mdl]
        mean = numpy.mean(line_data)
        sd = numpy.std(line_data)
        # QC values for extremes.
        for i in range(0,line_data.shape[0]):
            if line_data[i] < mean - 3 * sd or line_data[i] > mean + 3 * sd:
                line_data[i] = numpy.nan
        line_data_deg_c = (line_data - 273.15)
        plt.plot(line_data_deg_c,COLORS[mdl],lw=0.50,
                 marker='o',markersize=2)
    # Plot the freezing point line. TODO: Check if this is within the y-axis limits.
    plt.plot([0,h85_data.shape[2] - 1],[0,0],color='r',lw=1)
    # Set a reasonable number of y-axis ticks.
    y_max = numpy.max(plt.yticks()[0])
    y_min = numpy.min(plt.yticks()[0])
    step = numpy.arange(y_min,y_max,int(5 * round((y_max - y_min) / 5)))
    plt.yticks(numpy.arange(y_min, y_max, step))
    # Set the y-axis label.
    plt.ylabel(u'850-mb (\u00b0C)')
    # Define axis for 700 mb temperatures.
    plt.axes([0.1500, 0.1500, 0.8000, 0.1875])
    # Set the x-axis of the plot. (where,what,size in points).
    plt.xticks(numpy.arange(0, sfc_data.shape[2]),labels,size=10)
    # Draw the true plot.
    # Loop over all models (shape[1]).
    for mdl in range(0,sfc_data.shape[1]):
        line_data = h70_data[config.indexes['t']][mdl]
        mean = numpy.mean(line_data)
        sd = numpy.std(line_data)
        # QC values for extremes.
        for i in range(0,line_data.shape[0]):
            if line_data[i] < mean - 3 * sd or line_data[i] > mean + 3 * sd:
                line_data[i] = numpy.nan
        line_data_deg_c = (line_data - 273.15)
        plt.plot(line_data_deg_c,COLORS[mdl],lw=0.50,
                 marker='o',markersize=2)
    # Plot the freezing point line. TODO: Check if this is within the y-axis limits.
    plt.plot([0,h70_data.shape[2] - 1],[0,0],color='r',lw=1)
    # Set a reasonable number of y-axis ticks.
    y_max = numpy.max(plt.yticks()[0])
    y_min = numpy.min(plt.yticks()[0])
    step = int(5 * round(((y_max - y_min) / 5.0) / 5.0))
    plt.yticks(numpy.arange(y_min, y_max, step))
    # Set the y-axis label.
    plt.ylabel(u'700-mb (\u00b0C)')
    # TODO: Add 850 and 700 mb levels.
    #
    #
    # Plot the title panel.
    plt.axes([0.25, 0.9, 0.7, 0.1], frameon=False, axisbg='w')
    plt.xticks([]), plt.yticks([])
    plot_title = '%s Ensemble Member Forecast Initialized %s\nInstantaneous %s'\
                 ' Hourly Temperatures coded by EFS\nColors represent individu'\
                 'al member models.'\
                 % (config.forecast_system.upper(),
                    config.model_init_dt.strftime('%HZ%d%b%Y').upper(),
                    config.model_fcst_interval)
    plt.text(0.5,0.5,plot_title,ha='center',va='center',size=10,color='#8200dc')
    plt.savefig(output_file_path)
    plt.clf()
    return
#
def plot_null(*args):
    """
    Dummy plot for multiple data height levels.
    """
    pass
#
if __name__ == '__main__':
    print 'temps.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF