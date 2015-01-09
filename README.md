PyWxFADES
=========

Python Weather Forecast Analysis and Display for Ensemble Systems

This program will analyze ensemble forecast system data and produce plume
diagrams for various fields. This is a rewrite of some legacy precipitation-
type plume code written a year ago. The goal of this rewrite is to create a
framework for extensibility.

The initial goal will be for this program to be able to recreate the plumes
created by the original code. A sample graphic is provided in this repository.
After this is accomplished, the code will be extended to produce graphics for
other types of data as well. One major suggestion is temperature plumes at
various pressure levels. Thus, one major goal for this project is to create
very extensible code to expedite the addition of new graphic processes.

Version 1.0 will be able to recreate the plumes created by the original code.

Note, this project makes use of the following external modules:
Pygrib
matplotlib
numpy

The process:
In automatic mode, explore available data and find the latest data to process.
Manual mode may use command line arguments, or a text-based user interface to
 choose between specific dates, times, forecast systems, data types, etc.
Initial setup is done, configuration class is initialized with several pieces
 of data, such as the data directory, model run information, etc.
Station data objects are created for each station.
Model data objects are created for each data file.
Model data files are opened and data are added to station data objects.
Plumes are plotted once all data are entered.
Cleanup and possibly transfer graphics to a web server.

Things I think will be necessary:
-Main/Entry:
 This is functional programming which will have the process running the entire
 program. This should read command line arguments, set up config and issue
 commands to other parts of the program.
 For now, the focus should be on locally stored data, but this could be
 extended to check data stored on NCEP servers and automatically downloading
 data directly from that source.
-Configuration class:
 Several variables in the runtime environment control how the program behaves.
 Many parts of the program rely on knowing information such as the model
 initialization time, the forecast system in use, stations to use, etc.
 It makes sense to bottle these settings into a single object which may be
 easily passed from one part of the program to another. There will also be
 quality control functions for defining these settings, in case user input does
 not produce a viable data source.
-Station data:
 Stations are locations at which plumes will be plotted from nearby grid points.
 Since each station has several attributes, such as location, and name, as well
  as data, once processing begins, it makes sense to create an object for each
  station.
-Precip Stats:
 This class was implemented in the original code, but may be handled just as
  well by defining these functions within the station data class. This will
  manage the statistics for the side panel of precip-type plumes.
-Model data:
 Since each data file has certain attributes, such as the model it came from,
  name, and location of the file on the file system, as well as functions for
  reading the files and managing the data being drawn from the files, it makes
  sense to make this an object. This should handle accessing and retrieving
  data, and distributing data to station data objects.
  
More classes may be added as I think of them.