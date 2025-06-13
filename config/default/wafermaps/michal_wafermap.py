global wafer_parameters


# Configuration wafer parameters
wafer_name = "MICHAL"
wafer_size = 2
xsize = 62.5
ysize = 62.5
nchips = 4
nmodules = 16

real_origin_chip = "-10 -26"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['BOTTOM-LEFT', 'BI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-351, 1', '-447, -527', '97, -527']
# distances from chip origin
wafer_modules = ['0.0 0.0', '-600.0 0.0', '-600.0 0.0', '-600.0 0.0', '1800.0 -600.0', '-600.0 0.0', '-600.0 0.0', '-600.0 0.0', '1800.0 -600.0', '-600.0 0.0', '-600.0 0.0', '-600.0 0.0', '1800.0 -600.0', '-600.0 0.0', '-600.0 0.0', '-600.0 0.0']
# modules name
wafer_modules_name = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16']

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