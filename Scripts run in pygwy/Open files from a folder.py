#
## Opens all files from a certain folder.
## Don't forget to change the directory.
#

import os

# Define the folder's directory
os.chdir(r'[INPUT YOUR DIRECTORY HERE]')
location = os.getcwd()

# Make a list from the files' names in the folder
files = os.listdir(location)

# Open each and every file from the folder
for i in range(len(files)) :
	container = gwy.gwy_app_file_load(files[i])
