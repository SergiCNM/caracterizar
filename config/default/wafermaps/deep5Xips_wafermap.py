global wafer_parameters


# Configuration wafer parameters
wafer_name = "DEEP"
wafer_size = 8
xsize = 6938.8
ysize = 5543.4
nchips = 5
nmodules = 1

real_origin_chip = "-14 -4"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "-4 3" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-RIGHT', 'BI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '11 -14', '0 -14', '-10 -14', '0 -25']
# distances from chip origin
wafer_modules = ['0.0 0.0']
wafer_modules_name = ['1']

# wafer parameters
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
"wafer_modules_name": wafer_modules_name,
"real_origin_chip": real_origin_chip,
"navigation_options": navigation_options

}