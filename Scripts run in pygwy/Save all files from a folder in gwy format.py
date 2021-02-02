#
## This script loads all files from a specific folder and saves them in 
## gwyddion native format.
## Don't forget to change the directory.
#

import os, glob

# Define the folder's directory
os.chdir(r'[INPUT YOUR DIRECTORY HERE]')
location = os.getcwd()

# Make a list from the files' names in the folder
files = os.listdir(location)

# Load each and every file from the folder and save it in gwy format
for i in range(len(files)) :
	
	try :
		container = gwy.gwy_file_load(files[i], gwy.RUN_NONINTERACTIVE)
		gwy.gwy_app_data_browser_add(container)
		new_filename = str(i) + ".gwy"
		gwy.gwy_file_save(container, new_filename, gwy.RUN_NONINTERACTIVE)
		gwy.gwy_app_data_browser_remove(container)
	
	except Exception:
		sys.exc_clear()
