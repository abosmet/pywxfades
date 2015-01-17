PyWxFADES
=========

Python Weather Forecast Analysis and Display for Ensemble Systems

This is a stand-alone program capable of generating plume diagrams from ensemble
forecast data. Currently the GEFS and SREF systems are supported. The program's
data retrieval and referencing routines are designed to be extensible and create
new types of plumes from basic prescriptions as they are designed and
implemented.

Note, this project makes use of the following external modules:
pygrib
matplotlib
numpy

Note, also, that this program is designed to be run in a linux environment only.
It has not been tested on Windows or Mac.

To run this program, set up a directory structure as example below:

	program/

		config/ ## stations data files here
	
			*.dat
		
		GRIB/	## Raw data (grib2 format) here
	
			20150112/
		
				sref/
			
					09/
				
						*.grib2
					
		output/	## Output graphics will go here
	
		src/	## Copy src directory from repository here
	
			pywxfades/
		
				*

