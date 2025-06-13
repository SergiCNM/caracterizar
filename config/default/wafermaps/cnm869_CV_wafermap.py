global wafer_parameters


# Configuration wafer parameters
wafer_name = "CNM869_CV"
wafer_size = 6
xsize = 5000.0
ysize = 5000.0
nchips = 183
nmodules = 1

real_origin_chip = "-12 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '3 -1', '0 -1', '-3 -1', '-6 -1', '3 -2', '0 -2', '-3 -2', '-6 -2', '-9 -2', '6 -3', '3 -3', '0 -3', '-3 -3', '-6 -3', '-9 -3', '6 -4', '3 -4', '0 -4', '-3 -4', '-6 -4', '-9 -4', '6 -5', '3 -5', '0 -5', '-3 -5', '-6 -5', '-9 -5', '-12 -5', '9 -6', '6 -6', '3 -6', '0 -6', '-3 -6', '-6 -6', '-9 -6', '-12 -6', '9 -7', '6 -7', '3 -7', '0 -7', '-3 -7', '-6 -7', '-9 -7', '-12 -7', '9 -8', '6 -8', '3 -8', '0 -8', '-3 -8', '-6 -8', '-9 -8', '-12 -8', '9 -9', '6 -9', '3 -9', '0 -9', '-3 -9', '-6 -9', '-9 -9', '-12 -9', '9 -10', '6 -10', '3 -10', '0 -10', '-3 -10', '-6 -10', '-9 -10', '-12 -10', '-15 -10', '9 -11', '6 -11', '3 -11', '0 -11', '-3 -11', '-6 -11', '-9 -11', '-12 -11', '-15 -11', '9 -12', '6 -12', '3 -12', '0 -12', '-3 -12', '-6 -12', '-9 -12', '-12 -12', '-15 -12', '9 -13', '0 -13', '-3 -13', '-15 -13', '9 -14', '0 -14', '-3 -14', '-15 -14', '9 -15', '6 -15', '3 -15', '0 -15', '-3 -15', '-6 -15', '-9 -15', '-12 -15', '-15 -15', '9 -16', '6 -16', '3 -16', '0 -16', '-3 -16', '-6 -16', '-9 -16', '-12 -16', '-15 -16', '9 -17', '6 -17', '3 -17', '0 -17', '-3 -17', '-6 -17', '-9 -17', '-12 -17', '-15 -17', '9 -18', '6 -18', '3 -18', '0 -18', '-3 -18', '-6 -18', '-9 -18', '-12 -18', '9 -19', '6 -19', '3 -19', '0 -19', '-3 -19', '-6 -19', '-9 -19', '-12 -19', '9 -20', '6 -20', '3 -20', '0 -20', '-3 -20', '-6 -20', '-9 -20', '-12 -20', '9 -21', '6 -21', '3 -21', '0 -21', '-3 -21', '-6 -21', '-9 -21', '-12 -21', '6 -22', '3 -22', '0 -22', '-3 -22', '-6 -22', '-9 -22', '-12 -22', '6 -23', '3 -23', '0 -23', '-3 -23', '-6 -23', '-9 -23', '6 -24', '3 -24', '0 -24', '-3 -24', '-6 -24', '-9 -24', '3 -25', '0 -25', '-3 -25', '-6 -25', '-9 -25', '3 -26', '0 -26', '-3 -26', '-6 -26']
# distances from chip origin
wafer_modules = ['0 0']
# modules name
wafer_modules_name = ['0 0']

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