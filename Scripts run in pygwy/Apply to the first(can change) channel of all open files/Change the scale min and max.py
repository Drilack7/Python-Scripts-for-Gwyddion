#
## This script changes the min and max of the scale of the first channel of all open files.
## Change the default minimum_scale_value and maximum_scale_value, below in lines 11 and 12.
## The units are always in SI.
## For the process to apply to another channel, change the number in line 9 accordingly (0 is for first channel,
## 1 is for second channel, etc).
#

channel_to_process = 0

minimum_scale_value = -1e-07
maximum_scale_value = 1e-07

# Iterate over all open files and all channels
for container in gwy.gwy_app_data_browser_get_containers():

	# Makes this channel current in the data browser
	gwy.gwy_app_data_browser_select_data_field(container, channel_to_process)

	# Change the min and max of the color scale
	container.set_int32_by_name('/' + str(channel_to_process) + '/base/range-type', gwy.LAYER_BASIC_RANGE_FIXED)
	container.set_double_by_name('/' + str(channel_to_process) + '/base/min', minimum_scale_value)
	container.set_double_by_name('/' + str(channel_to_process) + '/base/max', maximum_scale_value)
