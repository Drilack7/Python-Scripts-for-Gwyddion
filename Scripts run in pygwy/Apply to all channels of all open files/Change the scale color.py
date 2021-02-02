#
## This script changes the color of the scale to all open files and all channels
## The default color is "Gwyddion.net" but can be changed in the code to any other color
## Change the last string in the last line ("Gwyddion.net") to any other of the colors available
#

# Iterate over all open files and all channels
for container in gwy.gwy_app_data_browser_get_containers():
	for i in gwy.gwy_app_data_browser_get_data_ids(container):
	
		# Makes this channel current in the data browser
		gwy.gwy_app_data_browser_select_data_field(container, i)
	
		# Change the color of the scale 
		container.set_string_by_name('/' + str(i) + '/base/palette', "Gwyddion.net")
