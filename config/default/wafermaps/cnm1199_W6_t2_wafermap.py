global wafer_parameters


# Configuration wafer parameters
wafer_name = "CNM1199_W6_t2"
wafer_size = 6
xsize = 2900.0
ysize = 2900.0
nchips = 89
nmodules = 1

real_origin_chip = "-3 -23"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '0 -1', '0 -2', '-1 -2', '0 -3', '-1 -3', '-2 -3', '0 -4', '-1 -4', '-2 -4', '0 -5', '-1 -5', '-2 -5', '-3 -5', '0 -6', '-1 -6', '-2 -6', '-3 -6', '-1 -7', '-2 -7', '-3 -7', '-4 -7', '-1 -8', '-2 -8', '-3 -8', '-4 -8', '-1 -9', '-2 -9', '-3 -9', '-4 -9', '-5 -9', '-1 -10', '-2 -10', '-3 -10', '-4 -10', '-5 -10', '-6 -10', '-2 -11', '-3 -11', '-4 -11', '-5 -11', '-6 -11', '-2 -12', '-3 -12', '-4 -12', '-5 -12', '-6 -12', '-7 -12', '-3 -13', '-4 -13', '-5 -13', '-6 -13', '-7 -13', '-3 -14', '-4 -14', '-5 -14', '-6 -14', '-7 -14', '-8 -14', '-4 -15', '-5 -15', '-6 -15', '-7 -15', '-8 -15', '-5 -16', '-6 -16', '-7 -16', '-8 -16', '-9 -16', '-6 -17', '-7 -17', '-8 -17', '-9 -17', '-10 -17', '-7 -18', '-8 -18', '-9 -18', '-10 -18', '-8 -19', '-9 -19', '-10 -19', '-11 -19', '-9 -20', '-10 -20', '-11 -20', '-10 -21', '-11 -21', '-12 -21', '-12 -22']
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