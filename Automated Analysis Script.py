##
# This script loads in gwyddion software all files from a folder, flattens the images with the largest scan size 
# and calculates the mean depth of the image. It also creates new files with different names in gwyddion
# format and jpeg images of the channel of internest and also creates a collage of all these images.
##

import os, re, sys
from collage_maker import make_collage

# Use the following directory for importing modules
sys.path.append("C:/Program Files (x86)/Gwyddion/bin")

# Import the gwy module before running the scripts
import gwy

# Define function to get average of a list 
def Average(lst): 
    return sum(lst) / len(lst)

# Define function for sorting the list of the filenames
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

print("\nPlease enter the files' folrder directory:")
print("(Example: 'C:\Users\username\Desktop\dataset')")
directory = str(raw_input())
# Change the current folder's directory and get the name
os.chdir(directory)
location = os.getcwd()

# Make a list from the filenames in the folder in alphanumerical order
all_files = sorted_alphanumeric(os.listdir(location))

# Create a list for only the files gwyddion can open
files = []

# Create the list with the scan sizes
sizes = []

# Create the list with the current(I) images for the collage
images = []

# Create the lists of min and max current values for the scale of current maps
minimum_current_values = []
maximum_current_values = []

# Input the morphology channel and channel of internet (current) numbers
print("Please enter the morphology channel number (e.g. 0 for first channel, 1 for second, etc.): ")
morphology_channel = int(raw_input())
print("Please enter the channel of interest number (e.g. 0 for first channel, 1 for second, etc.): ")
interest_channel = int(raw_input())

# Load all files from the folder and fill the lists we created
for i in range(len(all_files)) :
	
	try :
		# Load the files of the folder and add them to the data browser
		container = gwy.gwy_file_load(all_files[i], gwy.RUN_NONINTERACTIVE)
		gwy.gwy_app_data_browser_add(container)
		# Get the morphology channel data field
		data_field = container['/' + str(morphology_channel) + '/data']
		# Get the width physical dimension (scan size)
		xreal = data_field.get_xreal()
		# Fill the list with the scan sizes
		sizes.append(xreal)
		
		# Fill the lists with the current channel min and max values
		current_data_field = container['/' + str(interest_channel) + '/data']
		Imin = current_data_field.get_min()
		Imax = current_data_field.get_max()
		minimum_current_values.append(Imin)
		maximum_current_values.append(Imax)
		
		# Create a list with only the files gwyddion can open
		files.append(all_files[i])

		# Remove the file (container) from the data browser to avoid overloading the memory
		gwy.gwy_app_data_browser_remove(container)
		
	except Exception:
		sys.exc_clear()

# Calculate the max scan size
max_size = max(sizes)

# Create the counter for the large scan-size images
readout_number = 1

# Initiate the depth variable
depth_in_nm = 0

# Open all large scan-size images from the folder
for i in range(len(files)) :
	
	# Load the files of the list 'files' and add them to the data browser
	container = gwy.gwy_file_load(files[i], gwy.RUN_NONINTERACTIVE)
	gwy.gwy_app_data_browser_add(container)
	
	# Get the morphology channel data field and width physical dimension (scan size)
	data_field = container['/' + str(morphology_channel) + '/data']
	xreal = data_field.get_xreal()
	
	# Open only the large scan-size images
	if xreal == max_size :

		# Make this channel current (active) in the data browser (so, everything applies to this one)
		gwy.gwy_app_data_browser_select_data_field(container, morphology_channel)
				
		# Get the pixel width and height and image aspect ratio
		xres = data_field.get_xres()
		yres = data_field.get_yres()
		aspect_ratio = xres/yres

		# Decide the margins of the mask
		if aspect_ratio > 5 :
			x_margin = 30
			y_margin = 0
		else :
			x_margin = 15
			y_margin = 5

		# Create a clone -zero filled- data field for the mask and fill it
		mask_field = data_field.new_alike()
		mask_field.area_fill(x_margin, y_margin, xres-2*x_margin, yres-2*y_margin, 1)

		for a in range(xres) :
			for b in range(yres) :
				if mask_field.get_val(a, b) == 1 :
					mask_field.set_val(a, b, 0)
				else :
					mask_field.set_val(a, b, 1)

		# Apply the mask's data field
		container['/' + str(morphology_channel) + '/mask'] = mask_field

		# Level, including the mask
		coeffs = data_field.area_fit_plane(mask_field, 0, 0, xres-1, yres-1)
		data_field.plane_level(*coeffs)

		# Zero mean value, including the mask
		data_field.add(-data_field.area_get_avg(mask_field, 0, 0, xres-1, yres-1))
		data_field.data_changed()
				
		# Get the deepest point value and calculate the critical value
		minimum = data_field.get_min()
		critical_value = minimum*2/3

		# Create a clone of the data field and put it as mask
		mask2_field = data_field.duplicate()
		container['/' + str(morphology_channel) + '/mask'] = mask2_field

		# Mask the points with values less than 2/3 of the minimum
		data = mask2_field.get_data()
		for j in range(len(data)) :
			if data[j] < critical_value :
				data[j] = 1
			else :
				data[j] = 0
		mask2_field.set_data(data)

		# Calculate the average depth of the masked region and transform to nm
		depth_in_m = data_field.area_get_avg(mask2_field, 0, 0, xres-1, yres-1)
		depth_in_nm = depth_in_m * 1000000000

		# Define the new filename and save the file in gwyddion format
		new_filename = str(i+1) + ") channel-1 " + str(readout_number) + " (Depth=%.1f nm)" % depth_in_nm + ".gwy"
		gwy.gwy_file_save(container, new_filename, gwy.RUN_NONINTERACTIVE)
		
		# Print the depth of each file
		print("Image " + files[i] + ": Average depth = %.1f nm" % depth_in_nm)
		
		# Increment the read-out filename number
		readout_number = readout_number + 1

		# Remove the container from the memory
		gwy.gwy_app_data_browser_remove(container)
		
	else :
		# Make this channel current (active) in the data browser (so, everything applies to this one)
		gwy.gwy_app_data_browser_select_data_field(container, interest_channel)

		# Change the color of the scale 
		container.set_string_by_name('/' + str(interest_channel) + '/base/palette', "Gwyddion.net")

		# Create and fill a new list with only the first half of the minimum current values
		half_minimum_current_values = []
		for element in range(int(len(minimum_current_values)/2)) :
			half_minimum_current_values.append(minimum_current_values[element])

		# Create and fill a new list with only the first half of the maximum current values
		half_maximum_current_values = []
		for element in range(int(len(maximum_current_values)/2)) :
			half_maximum_current_values.append(maximum_current_values[element])
		
		# Change the min and max of the color scale
		container.set_int32_by_name('/' + str(interest_channel) + '/base/range-type', gwy.LAYER_BASIC_RANGE_FIXED)
		container.set_double_by_name('/' + str(interest_channel) + '/base/min', Average(half_minimum_current_values))
		container.set_double_by_name('/' + str(interest_channel) + '/base/max', Average(half_maximum_current_values))

                # Define the new filename and save the file in gwyddion format and jpg
		new_filename = str(i+1) + ") channel-2"
		gwy.gwy_file_save(container, new_filename + ".gwy", gwy.RUN_NONINTERACTIVE)
		gwy.gwy_file_save(container, new_filename + ".jpg", gwy.RUN_NONINTERACTIVE)

		# Fill the list for the image collage
		images.append(new_filename + ".jpg")

		# Remove the container from the memory
		gwy.gwy_app_data_browser_remove(container)


# Make the collage of all the current (channel 1) images with the same scale
make_collage(images, "collage.jpg", 1600, 250)
