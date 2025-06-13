#            Wafermap 5 CAPS to test
#             -------------------
#            | 1 | 2 | 3 | 4 | 5 |
#             -------------------


global wafer_parameters


# Configuration wafer parameters
wafer_name = "CAP 6"
wafer_size = 4.000000
xsize = 2790.000000
ysize = 1950.000000
xmax = 6
ymax = 1
nchips = 6
nmodules = 2

real_origin_chip = "-10 -4"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "-6 -12" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270


# wafer positions
wafer_positions = []
wafer_positions = np.append(wafer_positions,["0 0","-3 0","-6 0","-9 0","-12 0", "-15 0"])
# wafer_positions = np.append(wafer_positions,["-15 -4","-12 -4","-9 -4","-6 -4","-3 -4","0 -4","3 -4"])
# wafer_positions = np.append(wafer_positions,["6 -8","3 -8","0 -8","-3 -8","-6 -8","-9 -8","-12 -8","-15 -8","-18 -8"])
# wafer_positions = np.append(wafer_positions,["-18 -12","-15 -12","-12 -12","-9 -12","-6 -12","-3 -12","0 -12","3 -12","6 -12"])
# wafer_positions = np.append(wafer_positions,["9 -16","6 -16","3 -16","0 -16","-3 -16","-6 -16","-9 -16","-12 -16","-15 -16","-18 -16","-21 -16"])
# wafer_positions = np.append(wafer_positions,["-21 -20","-18 -20","-15 -20","-12 -20","-9 -20","-6 -20","-3 -20","0 -20","3 -20","6 -20","9 -20"])
# wafer_positions = np.append(wafer_positions,["9 -24","6 -24","3 -24","0 -24","-3 -24","-6 -24","-9 -24","-12 -24","-15 -24","-18 -24","-21 -24"])
# wafer_positions = np.append(wafer_positions,["-21 -28","-18 -28","-15 -28","-12 -28","-9 -28","-6 -28","-3 -28","0 -28","3 -28","6 -28","9 -28"])
# wafer_positions = np.append(wafer_positions,["6 -32","3 -32","0 -32","-3 -32","-6 -32","-9 -32","-12 -32","-15 -32","-18 -32"])
# wafer_positions = np.append(wafer_positions,["-18 -36","-15 -36","-12 -36","-9 -36","-6 -36","-3 -36","0 -36","3 -36","6 -36"])
# wafer_positions = np.append(wafer_positions,["3 -40","0 -40","-3 -40","-6 -40","-9 -40","-12 -40","-15 -40"])
# wafer_positions = np.append(wafer_positions,["-12 -44","-9 -44","-6 -44","-3 -44","0 -44"])

# distances from chip origin
wafer_modules = ["0.00 0.00", "1000.00 1000.00"]


# wafer parameters (array with 14 parameters)
wafer_parameters = [wafer_name, wafer_size, xsize, ysize, xmax, ymax, nchips, nmodules, origin_chip, home_chip, flat_orientation, wafer_positions, wafer_modules, real_origin_chip]







