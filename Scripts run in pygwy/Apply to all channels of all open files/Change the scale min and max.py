#
## This script changes the min and max of the scale to all open files and all channels
## Change the the default minimum_scale_value and maximum_scale_value, right below in lines 7 and 8
## The units are always in SI 
#

minimum_scale_value = -1e-07
maximum_scale_value = 1e-07

# Iterate over all open files and all channels
for container in gwy.gwy_app_data_browser_get_containers():
	for i in gwy.gwy_app_data_browser_get_data_ids(container):
	
		# Makes this channel current in the data browser
		gwy.gwy_app_data_browser_select_data_field(container, i)
	
		# Change the min and max of the color scale
		container.set_int32_by_name('/' + str(i) + '/base/range-type', gwy.LAYER_BASIC_RANGE_FIXED)
		container.set_double_by_name('/' + str(i) + '/base/min', minimum_scale_value)
		container.set_double_by_name('/' + str(i) + '/base/max', maximum_scale_value)