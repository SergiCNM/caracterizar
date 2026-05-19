global wafer_parameters


# Configuration wafer parameters
wafer_name = "Gabriele"
wafer_size = 4
xsize = 15000.0
ysize = 15000.0
nchips = 24
nmodules = 3

real_origin_chip = "-2 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
init_chip = 1
end_chip = 24
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 0', '1 -1', '0 -1', '-1 -1', '-2 -1', '2 -2', '1 -2', '0 -2', '-1 -2', '-2 -2', '-3 -2', '2 -3', '1 -3', '0 -3', '-1 -3', '-2 -3', '-3 -3', '1 -4', '0 -4', '-1 -4', '-2 -4', '0 -5', '-1 -5']
# distances from chip origin
wafer_modules = ['0.0 0.0', '-3070.0 0.0', '-3070.0 0.0']
# modules name
wafer_modules_name = ['0 0', '0.000000 0.000000', '0.000000 0.000000']

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
"init_chip": init_chip,
"end_chip": end_chip,
"flat_orientation": flat_orientation,
"wafer_positions": wafer_positions,
"wafer_modules": wafer_modules,
"wafer_modules_name": wafer_modules_name,
"real_origin_chip": real_origin_chip,
"navigation_options": navigation_options

}