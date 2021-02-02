#
## This script changes the color of the scale to the first channel of all open files 
## The default color is "Gwyddion.net" but can be changed in the code to any other color
## Change the last string in the last line ("Gwyddion.net") to any other of the colors available
## For the process to apply to another channel, change the number in line 9 accordingly (0 is for first channel,
## 1 is for second channel, etc)
#

channel_to_process = 0

# Iterate over all open files and all channels
for container in gwy.gwy_app_data_browser_get_containers():
	
	# Makes this channel current in the data browser
	gwy.gwy_app_data_browser_select_data_field(container, channel_to_process)

	# Change the color of the scale 
	container.set_string_by_name('/' + str(channel_to_process) + '/base/palette', "Gwyddion.net")
