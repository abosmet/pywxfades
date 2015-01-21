'''
Created on Jan 7, 2015

@author: Joel
'''
# Local package from imports
from config import Config
from manageData import localInventory
from manageData import remoteInventory
# Standard library from imports
from glob import glob
# Standard library imports
import os
# Module constants
PRETEXT = '[UI]'
# Begin module code.
def display_menu(options,title='Menu',desc=None,multi=False):
    """
    Display a menu with from the given options. Individual options will be
     listed on separate lines indexed starting at 1 and incrementing by 1.
     Option number 10 will be indexed with 0. This function is not designed to
     create menues greater than length 10.
    Inputs:
        options <list>
         List of text options.
        title <string>
         Optional menu title.
        desc <string>
         Optional menu description.
        multi <boolean>
         Display panel navigation if set to True. Default False.
    Outputs:
        No physical outputs. Prints text to the terminal.
    """
    # Display blank line, then menu title.
    print '\n%s' % (title)
    # Print an underline under the title.
    print ''.join(['-' for i in title]) #@UnusedVariable
    # Show a description if one was sent.
    if desc:
        print desc,'\n'
    # Display options with indexes. Should give indexes 1-9 and 0 for index 10.
    print '\n'.join([(str((options.index(i) + 1) % 10) + ': ' + i) for i in\
                     options])
    # Display navigation when applicable.
    if multi:
        print "Enter 'p' for previous page, or 'n' for next page."
    print "Enter the number of your selection, or enter 'e' to quit."
    return
#
def get_run_input():
    """
    Create a menu from available model runs stored locally.
    Inputs:
        No physical inputs.
    Outputs:
        selection <string>
         Path of selected model run.
    """
    runs = localInventory.available_runs + remoteInventory.available_runs
    options = sorted([i[1] for i in runs], reverse = True)
    # Get user input and return selected option.
    option_index = menu(options, title = 'Please select a model run.',
                        desc = ' : Date\t\tHour\tSystem\tFiles\n : Ref: SREF: '\
                        '21 Files, GEFS: 943 or 1495 Files.')
    # Find proper run index given selected option.
    for run in runs:
        if run[1] == options[option_index]:
            run_index = runs.index(run)
    print '%s Selected model run:\n\t%s' % (PRETEXT, runs[run_index][1])
    # Create the local directories if a remote model run was selected.
    if len(runs[run_index]) == 3:
        if not os.path.exists(runs[run_index][0]):
            os.makedirs(runs[run_index][0])
    return runs[run_index][0]
#
def get_stations_data_file_input(config):
    """
    Finds available stations data files. Presents a menu for the user to make a
     selection. Returns the selected stations data file name (not the path).
    Inputs:
        config <Config> Config object containing runtime variables.
    Outputs:
        selection <string> The selected stations data file name.
    """
    #
    raw_glob = glob(Config.STATIONS_DATA_STORAGE_PATH + '/*.dat')
    # Loop over items and add to a new list if the item is a file.
    #  Grabs file name without its path.
    available_stations_data_files = [i.split('/')[-1] for i in raw_glob if\
                                     os.path.isfile(i)]
    # Get user input and return selected option.
    option_index = menu(available_stations_data_files,
                        title = 'Please select a stations data file.')
    return available_stations_data_files[option_index]
#
def menu(options,title='Menu',desc=None):
    """
    Generate a menu from a list of options and wait for a selection. After 10
     available options, generate another page of options.
    Inputs:
        options <list> 
         List of options from which to create a menu.
        title <String> 
         Menu title, defaults to 'Menu'
        desc <String> 
         Optional description for the menu
    Outputs:
        selection <int> Index of options item which the user selected.
    """
    # Split options into groups of 10.
    split_options = [options[i:i+10] for i in range(0, len(options), 10)]
    # Start panel index at 0.
    panel_index = 0
    # Keep going until a selection is made or the program terminates.
    while True:
        # Menu title should have page numbers when applicable.
        if len(split_options) > 1:
            menu_title = '%s Page %s of %s' % (title, panel_index + 1,
                                               len(split_options))
        else:
            menu_title = title
        # Display menu with current page of options.
        display_menu(split_options[panel_index], title = menu_title,
                      desc = desc, multi = (len(split_options) > 1))
        raw_selection = raw_input('Input: ')
        # Attempt to cast user input to an integer. Dodge ValueErrors.
        try:
            selection = int(raw_selection)
        except ValueError:
            selection = raw_selection
        # User wants to quit.
        if selection in ['e', 'E']:
            print "%s Program terminating at user's request." % (PRETEXT)
            print 'PYTHON STOP'
            exit()
        # User wants the next page. This can wrap around.
        elif len(split_options) > 1 and selection in ['n', 'N']:
            if panel_index == len(split_options) - 1:
                panel_index = 0
            else:
                panel_index += 1
        # User wants the previous page. This can wrap around.
        elif len(split_options) > 1 and selection in ['p', 'P']:
            if panel_index == 0:
                panel_index = len(split_options) - 1
            else:
                panel_index -= 1
        # User entered a possible selection.
        elif selection - 1 in range(0,len(split_options[panel_index])):
            if len(split_options[panel_index]) == 10 and selection == 0:
                selection = 10
            return (selection - 1) + (10 * panel_index)
        else:
            print '%s Input not recognized, please try again. . .\n' % (PRETEXT)
    #
#
def show(config):
    """
    Entry point of UI process.
    Process:
        -Menu to select a date from available dates.
        -Menu to select a forecast system from avail. systems at selected date.
        -Menu to select an initialization time from available times, given
          previous selections.
        -Eventually: Menu to select a plume type from available plume types.
        -Menu to select a stations data file from available data files.
    Inputs:
        config <Config> Config object which will be configured with UI inputs.
    Outputs:
        No physical outputs. Initializes the Config object.
    """
    # Get user's model run selection.
    input_path = get_run_input()
    # Set configuration using the selected path split at each folder.
    split_path = input_path.split('/')
    config.set_init_date(split_path[-3])
    config.set_forecast_system(split_path[-2])
    config.set_init_hour(split_path[-1])
    # Placeholder for plume type selection
    #
    #
    # Get the stations data file input.
    input_stations_data_file_name = get_stations_data_file_input(config)
    print '%s Selected stations data file:' % (PRETEXT),\
        input_stations_data_file_name
    config.set_stations_data_file_name(input_stations_data_file_name)
    return
#
if __name__ == '__main__':
    print 'ui.py is not designed to be run independently.'
    print 'PYTHON STOP'
#
#
#
#
# EOF