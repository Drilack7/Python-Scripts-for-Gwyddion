#
## This script changes the min and max of the scale of the current active image.
## Change the the default minimum_scale_value and maximum_scale_value, right below in lines 7 and 8
## The units are always in SI.
#

minimum_scale_value = -1e-07
maximum_scale_value = 1e-07

# Get the active image container, data field and number
container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
data_field = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
i = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)
	
# Makes this channel current in the data browser
gwy.gwy_app_data_browser_select_data_field(container, i)

# Change the min and max of the color scale
container.set_int32_by_name('/' + str(i) + '/base/range-type', gwy.LAYER_BASIC_RANGE_FIXED)
container.set_double_by_name('/' + str(i) + '/base/min', minimum_scale_value)
container.set_double_by_name('/' + str(i) + '/base/max', maximum_scale_value)