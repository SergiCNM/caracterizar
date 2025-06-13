global wafer_parameters


# Configuration wafer parameters
wafer_name = "SOLARMEMS"
wafer_size = 4
xsize = 5700.0
ysize = 5800.0
nchips = 175
nmodules = 1

real_origin_chip = "-6 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 0', '-2 0', '-3 0', '-4 0', '2 -1', '1 -1', '0 -1', '-1 -1', '-2 -1', '-3 -1', '-4 -1', '-5 -1', '-6 -1', '3 -2', '2 -2', '1 -2', '0 -2', '-1 -2', '-2 -2', '-3 -2', '-4 -2', '-5 -2', '-6 -2', '-7 -2', '4 -3', '3 -3', '2 -3', '1 -3', '0 -3', '-1 -3', '-2 -3', '-3 -3', '-4 -3', '-5 -3', '-6 -3', '-7 -3', '-8 -3', '4 -4', '3 -4', '2 -4', '1 -4', '0 -4', '-1 -4', '-2 -4', '-3 -4', '-4 -4', '-5 -4', '-6 -4', '-7 -4', '-8 -4', '5 -5', '4 -5', '3 -5', '2 -5', '1 -5', '0 -5', '-1 -5', '-2 -5', '-3 -5', '-4 -5', '-5 -5', '-6 -5', '-7 -5', '-8 -5', '-9 -5', '5 -6', '4 -6', '3 -6', '2 -6', '1 -6', '0 -6', '-1 -6', '-2 -6', '-3 -6', '-4 -6', '-5 -6', '-6 -6', '-7 -6', '-8 -6', '-9 -6', '5 -7', '3 -7', '2 -7', '1 -7', '0 -7', '-1 -7', '-2 -7', '-3 -7', '-4 -7', '-5 -7', '-6 -7', '-7 -7', '-9 -7', '5 -8', '4 -8', '3 -8', '2 -8', '1 -8', '0 -8', '-1 -8', '-2 -8', '-3 -8', '-4 -8', '-5 -8', '-6 -8', '-7 -8', '-8 -8', '-9 -8', '5 -9', '4 -9', '3 -9', '2 -9', '1 -9', '0 -9', '-1 -9', '-2 -9', '-3 -9', '-4 -9', '-5 -9', '-6 -9', '-7 -9', '-8 -9', '-9 -9', '4 -10', '3 -10', '2 -10', '1 -10', '0 -10', '-1 -10', '-2 -10', '-3 -10', '-4 -10', '-5 -10', '-6 -10', '-7 -10', '-8 -10', '4 -11', '3 -11', '2 -11', '1 -11', '0 -11', '-1 -11', '-2 -11', '-3 -11', '-4 -11', '-5 -11', '-6 -11', '-7 -11', '-8 -11', '3 -12', '2 -12', '1 -12', '0 -12', '-1 -12', '-2 -12', '-3 -12', '-4 -12', '-5 -12', '-6 -12', '-7 -12', '2 -13', '1 -13', '0 -13', '-1 -13', '-2 -13', '-3 -13', '-4 -13', '-5 -13', '-6 -13', '0 -14', '-1 -14', '-2 -14', '-3 -14', '-4 -14']
# distances from chip origin
wafer_modules = ['0 0']

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
"real_origin_chip": real_origin_chip,
"navigation_options": navigation_options

}