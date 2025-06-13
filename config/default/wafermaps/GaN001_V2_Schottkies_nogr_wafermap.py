global wafer_parameters


# Configuration wafer parameters
wafer_name = "GaN001_V2_Schottkies_nogr"
wafer_size = 2
xsize = 6600.0
ysize = 6600.0
nchips = 4
nmodules = 12

real_origin_chip = "-3 -2"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'BI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 -1', '1 -1', '0 -2']
# distances from chip origin
wafer_modules = ['0.0 0.0', '20.0 825.0', '50.0 925.0', '50.0 1050.0', '-2450.0 -2250.0', '-500.0 2350.0', '-270.0 1650.0', '-1465.0 150.0', '-53.0 -1000.0', '-12.0 -1000.0', '-13.0 -800.0', '-10.0 -800.0']
# modules name
wafer_modules_name = ['L30', 'L50', 'L100', 'L150', 'M2000', 'M1000', 'M500', 'R200', 'R100', 'R75', 'R50', 'R30']

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