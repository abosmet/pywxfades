'''
Created on Jan 11, 2015

@author: Joel
'''
# Local package imports.
import describe
# External package imports.
import matplotlib.pyplot as plt
import numpy
# Standard library from imports.
from datetime import datetime #@UnusedImport Needed type only.
from datetime import timedelta
# Standard library imports.
import os
#
# Define module constants.
COLORS = {'Rain':'g','Snow':'b','FZRA':'r',\
          'Sleet':'c','raw':'#8200dc','hourly':'0.5'}
# Begin module code.
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
    """
    # Import StationData/Config only when called to avoid redundancy errors.
    from stationData import StationData #@UnusedImport Need type only. @UnresolvedImport PyDev issue.
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
        now = config.model_init_dt + timedelta(hours=(i * config.model_fcst_interval))
        # Plot text every 24 for GEFS, every 12 hours for SREF, starting 0Z.
        # Year to be printed on first appearing label.
        # Date to be printed on all 0Z labels.
        # Empty string to be printed on all other labels.
        if now.hour == 0 or (now.hour == 12 and config.forecast_system == 'sref'):
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
            # TODELETE: Display debug text.
            print '[ptype] time: %s cum_amt: %s' % (tm,cum_amt)
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
                plt.plot([tm-1,tm],[prev_cum_amt,cum_amt],color)
        plt.plot(data[config.indexes['tp']][mdl],COLORS['hourly'],lw=0.25,marker='o',markersize=2)
    plt.ylabel('Precipitation(in)')
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