global wafer_parameters


# Configuration wafer parameters
wafer_name = "CNM1246_TIRA6"
wafer_size = 6
xsize = 9350.0
ysize = 3900.0
nchips = 33
nmodules = 12

real_origin_chip = "-7 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '0 -1', '0 -2', '0 -3', '0 -4', '0 -5', '0 -6', '0 -7', '0 -8', '0 -9', '0 -10', '0 -11', '0 -12', '0 -13', '0 -14', '0 -15', '0 -16', '0 -17', '0 -18', '0 -19', '0 -20', '0 -21', '0 -22', '0 -23', '0 -24', '0 -25', '0 -26', '0 -27', '0 -28', '0 -29', '0 -30', '0 -31', '0 -32']
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