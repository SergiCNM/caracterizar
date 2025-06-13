global wafer_parameters


# Configuration wafer parameters
wafer_name = "LAURAR_5"
wafer_size = 6
xsize = 6600.0
ysize = 5500.0
nchips = 25
nmodules = 1

real_origin_chip = "-2 -4"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-4 0', '-9 0', '-14 0', '-19 0', '0 -4', '-4 -4', '-9 -4', '-14 -4', '-19 -4', '0 -9', '-4 -9', '-9 -9', '-14 -9', '-19 -9', '0 -14', '-4 -14', '-9 -14', '-14 -14', '-19 -14', '0 -19', '-4 -19', '-9 -19', '-14 -19', '-19 -19']
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