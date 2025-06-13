global wafer_parameters


# Configuration wafer parameters
wafer_name = "CAP 104"
wafer_size = 4
xsize = 2790.0
ysize = 1950.0
nchips = 1
nmodules = 2

real_origin_chip = "-11 -3"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "-6 -12" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'BI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0']
# distances from chip origin
wafer_modules = ['0.000000 0.000000', '100.000000 0.000000']

# wafer parameters (array with 14 parameters)
wafer_parameters = {

"wafer_name": wafer_name,
"wafer_size": wafer_size,
"xsize": xsize,
"ysize": ysize,
"nchips": nchips,
"nmodules": nmodules,
"origin_chip": origin_chip,
"home_chip": home_chip,
"flat_orientation": flat_orientation,
"wafer_positions": wafer_positions,
"wafer_modules": wafer_modules,
"real_origin_chip": real_origin_chip,
"navigation_options": navigation_options

}