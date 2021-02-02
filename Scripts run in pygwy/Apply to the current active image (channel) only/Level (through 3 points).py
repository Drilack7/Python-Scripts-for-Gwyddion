#
## This script levels the current active image by fitting a plane through 3 points.
## The 3 points are: Top left corner, Bottom left and right corner.
## For this script to work, numpy Python module needs to be installed.
#

import numpy as np

# Get the active image container, data field and number
container = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER)
data_field = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD)
i = gwy.gwy_app_data_browser_get_current(gwy.APP_DATA_FIELD_ID)

# Get the pixel width and height
xres = data_field.get_xres()
yres = data_field.get_yres()

# Define the 3 points' coordinates 
(x1, y1) = (0,0)
(x2, y2) = (0,yres-1)
(x3, y3) = (xres-1,yres-1)

# Get the 3 points' values
z1 = data_field.get_val(x1,y1)
z2 = data_field.get_val(x2,y2)
z3 = data_field.get_val(x3,y3)

# Solve the matrix equation
M = np.array([ [x1,y1,1], [x2,y2,1], [x3,y3,1] ])
c = np.array([z1,z2,z3])
y = np.linalg.solve(M,c)

# Level the filed with the coefficients obtained by the solution
coeffs = [y[2], y[0], y[1]]
data_field.plane_level(*coeffs)
data_field.data_changed()
