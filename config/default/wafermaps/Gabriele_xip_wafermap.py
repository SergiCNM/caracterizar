global wafer_parameters


# Configuration wafer parameters
wafer_name = "Gabriele_xip"
wafer_size = 1
xsize = 3070.0
ysize = 3400.0
nchips = 3
nmodules = 16

real_origin_chip = "-3 -3"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
init_chip = 1
end_chip = 3
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 0', '-2 0']
# distances from chip origin
wafer_modules = ['0.0 0.0', '-730.0 0.0', '-730.0 0.0', '-730.0 0.0', '2190.0 800.0', '-730.0 0.0', '-730.0 0.0', '-730.0 0.0', '2190.0 950.0', '-730.0 0.0', '-730.0 0.0', '-730.0 0.0', '2190.0 800.0', '-730.0 0.0', '-730.0 0.0', '-730.0 0.0']
# modules name
wafer_modules_name = ['T1T', 'T2T', 'T3T', 'T4T', 'T1B', 'T2B', 'T3B', 'T4B', 'B1T', 'B2T', 'B3T', 'B4T', 'B1B', 'B2B', 'B3B', 'B4B']

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