global wafer_parameters


# Configuration wafer parameters
wafer_name = "GaN001_5000_Schottkies_wgr"
wafer_size = 2
xsize = 6600.0
ysize = 6600.0
nchips = 7
nmodules = 1

real_origin_chip = "-3 -2"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'BI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '2 -1', '0 -2', '-2 -2', '-2 -3', '0 -4', '-1 -4']
# distances from chip origin
wafer_modules = ['0 0']
# modules name
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