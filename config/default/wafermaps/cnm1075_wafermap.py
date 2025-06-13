global wafer_parameters


# Configuration wafer parameters
wafer_name = "CNM1075"
wafer_size = 6
xsize = 8370.0
ysize = 5850.0
nchips = 140
nmodules = 1

real_origin_chip = "-9 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '2 -1', '0 -1', '-2 -1', '-4 -1', '2 -2', '0 -2', '-2 -2', '-4 -2', '4 -3', '2 -3', '0 -3', '-2 -3', '-4 -3', '-6 -3', '4 -4', '2 -4', '0 -4', '-2 -4', '-4 -4', '-6 -4', '4 -5', '2 -5', '0 -5', '-2 -5', '-4 -5', '-6 -5', '4 -6', '2 -6', '0 -6', '-2 -6', '-4 -6', '-6 -6', '6 -7', '4 -7', '2 -7', '0 -7', '-2 -7', '-4 -7', '-6 -7', '-8 -7', '6 -8', '4 -8', '2 -8', '0 -8', '-2 -8', '-4 -8', '-6 -8', '-8 -8', '6 -9', '4 -9', '2 -9', '0 -9', '-2 -9', '-4 -9', '-6 -9', '-8 -9', '6 -10', '4 -10', '2 -10', '0 -10', '-2 -10', '-4 -10', '-6 -10', '-8 -10', '6 -11', '4 -11', '2 -11', '0 -11', '-2 -11', '-4 -11', '-6 -11', '-8 -11', '4 -12', '2 -12', '0 -12', '-2 -12', '-4 -12', '-6 -12', '6 -13', '4 -13', '2 -13', '0 -13', '-2 -13', '-4 -13', '-6 -13', '-8 -13', '6 -14', '4 -14', '2 -14', '0 -14', '-2 -14', '-4 -14', '-6 -14', '-8 -14', '6 -15', '4 -15', '2 -15', '0 -15', '-2 -15', '-4 -15', '-6 -15', '-8 -15', '6 -16', '4 -16', '2 -16', '0 -16', '-2 -16', '-4 -16', '-6 -16', '-8 -16', '6 -17', '4 -17', '2 -17', '0 -17', '-2 -17', '-4 -17', '-6 -17', '4 -18', '2 -18', '0 -18', '-2 -18', '-4 -18', '-6 -18', '4 -19', '2 -19', '0 -19', '-2 -19', '-4 -19', '-6 -19', '4 -20', '2 -20', '0 -20', '-2 -20', '-4 -20', '-6 -20', '2 -21', '0 -21', '-2 -21', '-4 -21']
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