global wafer_parameters


# Configuration wafer parameters
wafer_name = "CNM1114"
wafer_size = 4
xsize = 15030.0
ysize = 3050.0
nchips = 88
nmodules = 25

real_origin_chip = "-1 -6"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'BI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 0', '-2 0', '-3 0', '-3 -1', '-2 -1', '-1 -1', '0 -1', '0 -2', '-1 -2', '-2 -2', '-3 -2', '-3 -3', '-2 -3', '-1 -3', '0 -3', '0 -4', '-1 -4', '-2 -4', '-3 -4', '-3 -5', '-2 -5', '-1 -5', '0 -5', '0 -6', '-1 -6', '-2 -6', '-3 -6', '-3 -7', '-2 -7', '-1 -7', '0 -7', '0 -8', '-1 -8', '-2 -8', '-3 -8', '-3 -9', '-2 -9', '-1 -9', '0 -9', '0 -10', '-1 -10', '-2 -10', '-3 -10', '-3 -11', '-2 -11', '-1 -11', '0 -11', '0 -12', '-1 -12', '-2 -12', '-3 -12', '-3 -13', '-2 -13', '-1 -13', '0 -13', '0 -14', '-1 -14', '-2 -14', '-3 -14', '-3 -15', '-2 -15', '-1 -15', '0 -15', '0 -16', '-1 -16', '-2 -16', '-3 -16', '-3 -17', '-2 -17', '-1 -17', '0 -17', '0 -18', '-1 -18', '-2 -18', '-3 -18', '-3 -19', '-2 -19', '-1 -19', '0 -19', '0 -20', '-1 -20', '-2 -20', '-3 -20', '-3 -21', '-2 -21', '-1 -21', '0 -21']
# distances from chip origin
wafer_modules = ['0.0 0.0', '200.0 0.0', '400.0 0.0', '600.0 0.0', '800.0 0.0', '1000.0 0.0', '1200.0 0.0', '1400.0 0.0', '1600.0 0.0', '1800.0 0.0', '2000.0 0.0', '2200.0 0.0', '2400.0 0.0', '2600.0 0.0', '2800.0 0.0', '3000.0 0.0', '3200.0 0.0', '3400.0 0.0', '3600.0 0.0', '3800.0 0.0', '4000.0 0.0', '4200.0 0.0', '4400.0 0.0', '4600.0 0.0', '4800.0 0.0']

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