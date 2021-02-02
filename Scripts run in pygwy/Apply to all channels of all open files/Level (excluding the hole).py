#
## This script applies a big rectangular mask , levels the area (excl. mask)
## and applies "zero mean value" function (excl. mask) to all channels of all open files.
# 

# Iterate over all open files and all channels
for container in gwy.gwy_app_data_browser_get_containers():
	for i in gwy.gwy_app_data_browser_get_data_ids(container):
	
		# Makes this channel current in the data browser
		gwy.gwy_app_data_browser_select_data_field(container, i)
	
		# Get the current data field and active image number
		data_field = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
	

		# Get the pixel width and height and image aspect ratio
		xres = data_field.get_xres()
		yres = data_field.get_yres()
		aspect_ratio = xres/yres

		# Decide the margins of the mask
		if aspect_ratio > 5 :
			x_margin = int(xres/20)
			y_margin = 0
		else :
			x_margin = int(xres/20)
			y_margin = int(yres/20)

		# Create a clone -zero filled- data field for the mask and fill it
		mask_field = data_field.new_alike()
		mask_field.area_fill(x_margin, y_margin, xres-2*x_margin, yres-2*y_margin, 1)

		# Apply the mask's data field
		container['/' + str(i) + '/mask'] = mask_field

		# Access the modules settings file 
		settings = gwy.gwy_app_settings_get()

		# Level, excluding the mask
		settings['/module/level/mode'] = 0
		gwy.gwy_process_func_run('level', container, gwy.RUN_IMMEDIATE)

		# Zero mean value, excluding the mask
		settings['/module/zero_mean/mode'] = 0
		gwy.gwy_process_func_run('zero_mean', container, gwy.RUN_IMMEDIATE)
