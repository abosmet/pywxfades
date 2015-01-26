'''
Created on Jan 11, 2015

@author: Joel
'''
# Local package imports.
import describe
# External library imports.
import matplotlib.pyplot as plt
import numpy
# Standard library from imports.
from datetime import datetime #@UnusedImport Needed type only.
from datetime import timedelta
# Standard library imports.
import os
# Module constants
COLORS = {'Rain':'g','Snow':'b','FZRA':'r',\
          'Sleet':'c','raw':'#8200dc','hourly':'0.5'}
PRETEXT = '[PType]'
# Begin module code.
def gen_stats(raw_data,ref):
    """
    Generates precipitation statistics from available data.
    Inputs:
        data <numpy.ndarray>
         An array of shape (5,<num members>,<num forecasts>)
        ref <dict>
         Indexes dictionary from a config object.
    Outputs:
        statistics <tuple>
         Tuple in the form (mean rain, max rain, min rain, mean snow, max snow,
                            min snow, mean FZRA, max FZRA, min FZRA, mean sleet,
                            max sleet, min sleet, mean total, media total,
                            max total, min total)
    """
    # Copy data to a local array to avoid altering the true data.
    data = numpy.copy(raw_data)
    # Multiply precipitation amount by categorical precipitation type to get
    #  type-specific liquid-equivalent precipitation forecasts.
    for type_index in range(0,data.shape[0]):
        if type_index != ref['tp']:
            for mdl_index in range(0,data.shape[1]):
                data[type_index][mdl_index] =\
                    numpy.multiply(data[ref['tp']][mdl_index],
                                   data[type_index][mdl_index])
        else:
            pass
    # Define a new array without hourly data blocks to store totals only for
    #  each model.
    meta = numpy.zeros((data.shape[0],data.shape[1]),dtype='float')
    for type_index in range(0,data.shape[0]):
        for mdl_index in range(0,data.shape[1]):
            meta[type_index][mdl_index] = data[type_index][mdl_index].sum()
    # Generated statistics from meta and return.
    mean_rain = numpy.mean(meta[ref['crain']])
    max_rain = numpy.max(meta[ref['crain']])
    min_rain = numpy.min(meta[ref['crain']])
    mean_snow = numpy.mean(meta[ref['csnow']])
    max_snow = numpy.max(meta[ref['csnow']])
    min_snow = numpy.min(meta[ref['csnow']])
    mean_fzra = numpy.mean(meta[ref['cfrzr']])
    max_fzra = numpy.max(meta[ref['cfrzr']])
    min_fzra = numpy.min(meta[ref['cfrzr']])
    mean_sleet = numpy.mean(meta[ref['cicep']])
    max_sleet = numpy.max(meta[ref['cicep']])
    min_sleet = numpy.min(meta[ref['cicep']])
    mean_total = numpy.mean(meta[ref['tp']])
    med_total = numpy.median(meta[ref['tp']])
    max_total = numpy.max(meta[ref['tp']])
    min_total = numpy.min(meta[ref['tp']])
    return (mean_rain, max_rain, min_rain, mean_snow, max_snow, min_snow,
            mean_fzra, max_fzra, min_fzra, mean_sleet, max_sleet, min_sleet,
            mean_total, med_total, max_total, min_total)
#
def plot(sdo,config):
    """
    Plots a ptype plume from the data received.
    Process:
    For every model, at each forecast interval, plot a point at the current
     total precipitation value, and another point at the previous total
     precipitation value, then draw a line between them, colored according to
     the precipitation type variable at that time index.
     Also, plot another point at the total precipitation since last forecast
     point and draw a line between it and the previous forecast's precipitation.
    We need a plot_line function which takes 2 points and a color and draws a
     line between the points in the specified color.
    Inputs:
        sdo <StationData>
         StationData object for which this plume is being plotted.
        config <Config>
         Config object holding current runtime configuration settings.
    Outputs:
        No physical outputs. Writes an image file to disk.
    """
    # Import StationData/Config only when called to avoid redundancy errors.
    from stationData import StationData #@UnusedImport @UnresolvedImport
    #                                    ^ Need type only,^ Pydev issues
    from config import Config #@UnresolvedImport PyDev issue.
    # Define a few static values from config and station data.
    output_file_path = (Config.OUTPUT_PATH + '/' +
                        config.model_init_dt.strftime('%Y%m%d/%HZ') + '/' +
                        describe.PLUMES[0][0] + '-' + str(sdo.station_name) +
                        '.png')
    # Grab relevant data.
    data = sdo.data[config.indexes[describe.PLUMES[0][0]]] # COMPLEX
    # Define a plot area.
    plt.axes([0.25, 0.15, 0.65, 0.75])
    # Define horizontal (time) axis values. Automatic values are nonsensical.
    # Define label number for control flow and a list of label text.
    label_num = 0
    labels = []
    # Loop over all times create a label based on forecast time and conditions.
    for i in range(0,data.shape[2]):
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
    plt.xticks(numpy.arange(0, data.shape[2]),labels,size=10)
    # Draw the true plot.
    # Loop over all models (shape[1]).
    for mdl in range(0,data.shape[1]):
        # Define current and previous cumulative amount totals used for line
        #  plotting.
        prev_cum_amt = 0
        cum_amt = 0
        # Define current and previous color to continue coloring line after
        #  precipitation ends.
        prev_color = COLORS['raw']
        color = COLORS['raw']
        # Loop over all forecast times (shape[2]).
        for tm in range(0,data.shape[2]):
            # Copy old values to 'previous' variables.
            prev_cum_amt = cum_amt
            prev_color = color
            # Add the forecast precipitation to the cumulative total precip.
            cum_amt += data[config.indexes['tp']][mdl][tm]
            # Do not plot a plume line on the initialization.
            if tm != 0:
                # Set the line color based on precipitation type.
                if int(data[config.indexes['crain']][mdl][tm]):
                    color = COLORS['Rain']
                elif int(data[config.indexes['csnow']][mdl][tm]):
                    color = COLORS['Snow']
                elif int(data[config.indexes['cicep']][mdl][tm]):
                    color = COLORS['Sleet']
                elif int(data[config.indexes['cfrzr']][mdl][tm]):
                    color = COLORS['FZRA']
                else:
                    color = prev_color
                # Plot line from previous time to current time, previous
                #  accumulation to current accumulation, and color based on
                #  precipitation type at the current time.
                plt.plot([tm-1,tm],[prev_cum_amt,cum_amt],color=color)
        # Plot hourly precipitation (silver lines).
        plt.plot(data[config.indexes['tp']][mdl],COLORS['hourly'],lw=0.25,
                 marker='o',markersize=2)
    plt.ylabel('Precipitation(in)')
    # Define axis limits to QC automatic axis limits.
    max_y = numpy.max(plt.yticks()[0])
    min_y = numpy.min(plt.yticks()[0])
    max_x = numpy.max(plt.xticks()[0])
    min_x = numpy.min(plt.xticks()[0])
    # Remove negative y-axis values.
    if min_y < 0:
        plt.axis([min_x,max_x,0.0,max_y])
    # If no precipitation is expected, display text and set huge y-axis values.
    if max_y < 0.05:
        plt.yticks([0, 5, 10, 15, 20, 25, 30])
        plt.text(15, 15, 'ENTIRE GRID UNDEFINED', ha='center', va='center',
                 size=22, alpha=0.85)
    # Plot the title panel.
    plt.axes([0.25, 0.9, 0.7, 0.1], frameon=False, axisbg='w')
    plt.xticks([]), plt.yticks([])
    plot_title = '%s Ensemble Member Forecast Initialized %s\nInstantaneous %s'\
                 ' Hour Liquid-Equivalent Precip coded by EFS\nPrecip Accumula'\
                 'tion(Green:Rain Red:Ice Cyan:Mix Blue:Snow)'\
                 % (config.forecast_system.upper(),
                    config.model_init_dt.strftime('%HZ%d%b%Y').upper(),
                    config.model_fcst_interval)
    plt.text(0.5,0.5,plot_title,ha='center',va='center',size=10,color='#8200dc')
    # Plot the station information panel.
    plt.axes([0.25, 0.05, 0.65, 0.1], frameon=False, axisbg='w')
    plt.xticks([]),plt.yticks([])
    # Text is generated slightly differently depending on forecast system.
    station_text = 'Station Data Plot for: %s Coords: %02.02f %02.02f\nNearest'\
                   ' Point Coords: %02.02f %02.02f, Distance: %02.02f km' %\
                   (sdo.station_name, sdo.latitude, sdo.longitude, sdo.grib_lat,
                     sdo.grib_lon, sdo.get_dist_to_nearest_grid_point())
    plt.text(0.6, 0.15, station_text, ha='center', va='center', size=10,
             color='#8200dc')
    # Generate statistics.
    stats = gen_stats(data,config.indexes)
    # Plot the statistics panel
    plt.axes([0,0.06,0.2,1], frameon=False, axisbg='w')
    plt.xticks([]),plt.yticks([])
    plt.text(0.25, 0.8000, 'Precipitation\n(Inches)', ha='left', va='center',
             size=12, color='#8200dc')
    plt.text(0.25, 0.7000, 'Rain\n Mean:  {0:.2f}\n Max:   {1:.2f}\n Min:   {2'\
                           ':.2f}'.format(stats[0],stats[1],stats[2]), 
             ha='left', va='center', size=11, color='#00dc00')
    plt.text(0.25, 0.5725, 'Snow\n Mean:  {0:.2f}\n Max:   {1:.2f}\n Min:   {2'\
                           ':.2f}'.format(stats[3],stats[4],stats[5]), 
             ha='left', va='center', size=11, color='#1e3cff')
    plt.text(0.25, 0.4450, 'FZRA\n Mean:  {0:.2f}\n Max:   {1:.2f}\n Min:   {2'\
                           ':.2f}'.format(stats[6],stats[7],stats[8]), 
             ha='left', va='center', size=11, color='#fa3c3c')
    plt.text(0.25, 0.3175, 'Sleet\n Mean:  {0:.2f}\n Max:   {1:.2f}\n Min:   {'\
                           '2:.2f}'.format(stats[9],stats[10],stats[11]), 
             ha='left', va='center', size=11, color='#00c8c8')
    plt.text(0.25, 0.1775, 'Total\n Mean:  {0:.2f}\n Median {1:.2f}\n Max:   {'\
                           '2:.2f}\n Min:   {3:.2f}'.format(stats[12],
                                                            stats[13],
                                                            stats[14],
                                                            stats[15]),
             ha='left', va='center', size=11, color='#000000')
    # Create output directories if they don't exist.
    cur_output_path = '/'.join(output_file_path.split('/')[:-1])
    if not os.path.exists(cur_output_path):
        os.makedirs(cur_output_path)
    # Save the figure.
    plt.savefig(output_file_path)
    # Clear the figure to plot the next one.
    plt.clf()
    return
#
if __name__ == '__main__':
    print 'ptype.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF