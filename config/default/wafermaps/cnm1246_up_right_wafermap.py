global wafer_parameters


# Configuration wafer parameters
wafer_name = "CNM1246_UP_RIGHT"
wafer_size = 6
xsize = 9350.0
ysize = 3900.0
nchips = 92
nmodules = 12
init_chip = 1

real_origin_chip = "-8 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 0', '0 -1', '-1 -1', '-2 -1', '0 -2', '-1 -2', '-2 -2', '-3 -2', '0 -3', '-1 -3', '-2 -3', '-3 -3', '0 -4', '-1 -4', '-2 -4', '-3 -4', '-4 -4', '0 -5', '-1 -5', '-2 -5', '-3 -5', '-4 -5', '0 -6', '-1 -6', '-2 -6', '-3 -6', '-4 -6', '0 -7', '-1 -7', '-2 -7', '-3 -7', '-4 -7', '-5 -7', '0 -8', '-1 -8', '-2 -8', '-3 -8', '-4 -8', '-5 -8', '0 -9', '-1 -9', '-2 -9', '-3 -9', '-4 -9', '-5 -9', '0 -10', '-1 -10', '-2 -10', '-3 -10', '-4 -10', '-5 -10', '0 -11', '-1 -11', '-2 -11', '-3 -11', '-4 -11', '-5 -11', '0 -12', '-1 -12', '-2 -12', '-3 -12', '-4 -12', '-5 -12', '-6 -12', '0 -13', '-1 -13', '-2 -13', '-3 -13', '-4 -13', '-5 -13', '-6 -13', '0 -14', '-1 -14', '-2 -14', '-3 -14', '-4 -14', '-5 -14', '-6 -14', '0 -15', '-1 -15', '-2 -15', '-3 -15', '-4 -15', '-5 -15', '-6 -15', '0 -16', '-1 -16', '-2 -16', '-3 -16', '-4 -16', '-5 -16']
# distances from chip origin
wafer_modules = ['0.0 0.0', '-1300.0 0.0', '-1300.0 0.0', '-1300.0 0.0', '3900.0 1300.0', '-1300.0 0.0', '-1300.0 0.0', '-1300.0 0.0', '3900.0 1300.0', '-1300.0 0.0', '-1300.0 0.0', '-1300.0 0.0']
# modules name
wafer_modules_name = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']

# wafer parameters
wafer_parameters = {

"wafer_name": wafer_name,
"wafer_size": wafer_size,
"xsize": xsize,
"ysize": ysize,
"nchips": nchips,
"nmodules": nmodules,
"init_chip": init_chip,
"origin_chip": origin_chip,
"home_chip": home_chip,
"flat_orientation": flat_orientation,
"wafer_positions": wafer_positions,
"wafer_modules": wafer_modules,
"wafer_modules_name": wafer_modules_name,
"real_origin_chip": real_origin_chip,
"navigation_options": navigation_options

}