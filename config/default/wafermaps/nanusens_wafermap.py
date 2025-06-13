global wafer_parameters


# Configuration wafer parameters
wafer_name = "NANUSENS"
wafer_size = 8
xsize = 25056.0
ysize = 31388.0
nchips = 26
nmodules = 4

real_origin_chip = "-2 -1"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "0 0" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options
navigation_options = ['UPPER-LEFT', 'UNI-DIRECTIONAL', 'ROW']

# wafer positions
wafer_positions = ['0 0', '-1 0', '-2 0', '-3 0', '1 -1', '0 -1', '-1 -1', '-2 -1', '-3 -1', '-4 -1', '1 -2', '0 -2', '-1 -2', '-2 -2', '-3 -2', '-4 -2', '1 -3', '0 -3', '-1 -3', '-2 -3', '-3 -3', '-4 -3', '0 -4', '-1 -4', '-2 -4', '-3 -4']
# distances from chip origin (relatives)
wafer_modules = ['0.0 0.0', '0.0 450.0', '-13599.0 -450.0', '0.0 450.0']
wafer_modules_name = ['1', '2', '3', '4']

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