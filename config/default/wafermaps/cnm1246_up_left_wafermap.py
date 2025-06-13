global wafer_parameters


# Configuration wafer parameters
wafer_name = "CNM1246_UP_LEFT"
wafer_size = 6
xsize = 9350.0
ysize = 3900.0
nchips = 92
nmodules = 12

real_origin_chip = "-6 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 0', '1 -1', '0 -1', '-1 -1', '2 -2', '1 -2', '0 -2', '-1 -2', '2 -3', '1 -3', '0 -3', '-1 -3', '3 -4', '2 -4', '1 -4', '0 -4', '-1 -4', '3 -5', '2 -5', '1 -5', '0 -5', '-1 -5', '3 -6', '2 -6', '1 -6', '0 -6', '-1 -6', '4 -7', '3 -7', '2 -7', '1 -7', '0 -7', '-1 -7', '4 -8', '3 -8', '2 -8', '1 -8', '0 -8', '-1 -8', '4 -9', '3 -9', '2 -9', '1 -9', '0 -9', '-1 -9', '4 -10', '3 -10', '2 -10', '1 -10', '0 -10', '-1 -10', '4 -11', '3 -11', '2 -11', '1 -11', '0 -11', '-1 -11', '5 -12', '4 -12', '3 -12', '2 -12', '1 -12', '0 -12', '-1 -12', '5 -13', '4 -13', '3 -13', '2 -13', '1 -13', '0 -13', '-1 -13', '5 -14', '4 -14', '3 -14', '2 -14', '1 -14', '0 -14', '-1 -14', '5 -15', '4 -15', '3 -15', '2 -15', '1 -15', '0 -15', '-1 -15', '4 -16', '3 -16', '2 -16', '1 -16', '0 -16', '-1 -16']
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
"origin_chip": origin_chip,
"home_chip": home_chip,
"flat_orientation": flat_orientation,
"wafer_positions": wafer_positions,
"wafer_modules": wafer_modules,
"wafer_modules_name": wafer_modules_name,
"real_origin_chip": real_origin_chip,
"navigation_options": navigation_options

}