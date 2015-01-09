'''
Created on Jan 7, 2015

@author: Joel
'''
#
from glob import glob
from config import Config
#
import os
#
def get_date_input(config):
    """
    Finds available dates and presents a menu for the user to make a selection.
    Returns the selected option.
    Inputs:
        config <Config> Config object containing runtime variables.
    Outputs:
        selection <string> The selected date.
    """
    # Find items living in the grib storage directory and list them.
    raw_glob = glob(Config.GRIB_STORAGE_PATH + '/*')
    # Loop over all items living in the grib storage directory and add the name
    #  of the directory without its path if the item is a directory (Linux 
    #  Only!).
    available_dates = [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
    # Create a menu from the available dates options defined above and get user
    #  input. User input will be returned as an index to one of the options.
    option_index = menu(available_dates)
    # Return the selection using the index input by the user.
    return available_dates[option_index]
#
def get_efs_input(config):
    """
    Finds available forecast systems for the date in stored in config. Presents
     a menu for the user to make a selection. Returns the selected option.
    Inputs:
        config <Config> Config object containing runtime variables.
    Outputs:
        selection <string> The selected forecast system.
    """
    # Find items living in the grib storage directory, in the previously
    #  selected date sub-directory.
    raw_glob = glob(Config.GRIB_STORAGE_PATH + '/' + config.model_init_date + '/*')
    # Loop over items and add to a new list if the item is a directory.
    #  Grabs directory name without its path (Linux Only!).
    available_efs_systems = [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
    # Get user input and return selected option.
    option_index = menu(available_efs_systems)
    return available_efs_systems[option_index]
#
def get_hour_input(config):
    """
    Finds available initialization times given the date and forecast system
     stored in config. Presents a menu for the user to make a selection.
     Returns the selected forecast initialization time.
    Inputs:
        config <Config> Config object containing runtime variables.
    Outputs:
        selection <string> The selected initialization time.
    """
    # Find items living the grib storage directory, selected date sub-directory,
    #  selected EFS system sub-directory.
    raw_glob = glob(Config.GRIB_STORAGE_PATH + '/' + config.model_init_date + '/' + config.forecast_system + '/*')
    # Loop over items and add to a new list if the item is a directory.
    #  Grabs directory name without its path (Linux Only!).
    available_hours = [i.split('/')[-1] for i in raw_glob if os.path.isdir(i)]
    # Get user input and return selected option.
    option_index = menu(available_hours)
    return available_hours[option_index]
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
    available_stations_data_files = [i.split('/')[-1] for i in raw_glob if os.path.isfile(i)]
    # Get user input and return selected option.
    option_index = menu(available_stations_data_files)
    return available_stations_data_files[option_index]
#
def menu(options,title='Menu',desc=None,multi=False):
    """
    Generate a menu from a list of options and wait for a selection. After 10
     available options, generate another page of options.
    Inputs:
        options <list> List of options from which to create a menu
        title <String> Menu title, defaults to 'Menu'
        desc <String> Optional description for the menu
        multi <Bool> If true, this menu is part of a multi-menu interface.
    Outputs:
        selection <int> Index of options item which the user selected.
    """
    # If there are more than 10 possible options, extra menu screens will be
    #  needed to accommodate.
    if len(options) > 10:
        # Split the options into groups of 10.
        split_options = [options[i:i+10] for i in range(0, len(options), 10)]
        # Panel index will be used to keep track of which page of the full menu
        #  the user is on.
        panel_index = 0
        # Keep going until an escape input appears or the program is terminated.
        while True:
            # Create a new menu from the subset of options and get input.
            #  The multi kwarg adds text to the menu indicating how to move
            #  between pages.
            selection = menu(split_options[panel_index],title='%s page %s of %s' % (title,panel_index,len(split_options)),desc=desc,multi=True)
            # User wants the next page. Note that this can wrap around.
            if selection in ['n','N']:
                panel_index += 1
            # User wants the previous page. Note that this can wrap around.
            elif selection in ['p','P']:
                panel_index -= 1
            # User entered a selection, return it.
            elif selection in [str(i) for i in range(0,10)]:
                return int(selection) - 1 + (panel_index * 10)
            # The user is a troll, troll harder.
            else:
                print 'Input not recognized, please try again. . .'
    # A reasonable number of options was sent, create a menu.
    else:
        # Display menu title.
        print title
        print ''.join(['-' for i in title]) #@UnusedVariable List comprehension.
        # Show a description if one was sent.
        if desc:
            print desc
        # Display options with indexes.
        print '\n'.join([(str((options.index(i) + 1) % 10) + ': ' + i) for i in options])
        # If this is part of a set, display page navigation information.
        if multi:
            print "Enter 'p' for previous page, or 'n' for next page."
        # Display user input prompt.
        print "Enter the number of your selection, or enter 'e' to quit."
        input_ = raw_input('Input: ')
        # User wants to exit.
        if input_ in ['e','E']:
            print "Program terminating at user's request. . ."
            print 'PYTHON STOP'
            exit()
        # If this menu is part of a multi-menu structure, check for n or p
        #  indicating a change in menu. This will return to a higher iteration
        #  for processing.
        elif multi and input_ in ['n','p','N','P']:
            return input_
        # If neither of the above are true, attempt to cast user input to an
        #  integer. This will raise a ValueError if a string was entered. Also,
        #  raise a ValueError manually if the input did not match any available
        #  options. ValueErrors will cause the program to prompt again.
        else:
            try:
                # Attempt to cast to an integer.
                int_input = int(input_)
                # If casting succeeded, but the value doesn't match any
                #  available options, raise a ValueError.
                if int_input not in range(0,len(options)):
                    raise ValueError()
            except ValueError:
                # Display a message and retry input by calling up this function
                #  again with the same parameters.
                print 'Input not recognized or value out of range, please try again. . .'
                int_input = menu(options,title=title,desc=desc,multi=multi)
            finally:
                # Return int_input when it does succeed, either by error-
                #  handling or by running correctly.
                return int_input
            #
        #
    # All code reaching the end of this function will have returned or exited,
    #  no syntax necessary for closing out the function.
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
    # Get the date input and set config.
    input_date = get_date_input(config)
    config.set_init_date(input_date)
    # Get the EFS system input and set config.
    input_forecast_system = get_efs_input(config)
    config.set_forecast_system(input_forecast_system)
    # Get the initialization time input and set config.
    input_init_time = get_hour_input(config)
    config.set_init_hour(input_init_time)
    # Placeholder for plume type selection
    #
    #
    # Get the stations data file input.
    input_stations_data_file_name = get_stations_data_file_input(config)
    config.set_stations_data_file_name(input_stations_data_file_name)
    config.expand()
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