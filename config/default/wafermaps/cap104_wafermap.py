#              Wafermap 104 CAPS
#             -------------------
#            | 1 | 2 | 3 | 4 | 5 |
#         ---------------------------
#        | 12| 11| 10| 9 | 8 | 7 | 6 |
#     -----------------------------------
#  	 | 13| 14| 15| 16| 17| 18| 19| 20| 21|
#     -----------------------------------
#  	 | 30| 29| 28| 27| 26| 25| 24| 23| 22|
#   -------------------------------------------
#  | 31| 32| 33| 34| 35| 36| 37| 38| 39| 40| 41|
#   -------------------------------------------
#  | 52| 51| 50| 49| 48| 47| 46| 45| 44| 43| 42|
#   -------------------------------------------
#  | 53| 54| 55| 56| 57| 58| 59| 60| 61| 62| 63|
#   -------------------------------------------
#  | 74| 73| 72| 71| 70| 69| 68| 67| 66| 65| 64|
#   -------------------------------------------
#      | 75| 76| 77| 78| 79| 80| 81| 82| 83|
#   	-----------------------------------
#  	   | 92| 91| 90| 89| 88| 87| 86| 85| 84|
#   	-----------------------------------
#          | 93| 94| 95| 96| 97| 98| 99|
#           ---------------------------
#              |104|103|102|101|100|
#               -------------------

global wafer_parameters


# Configuration wafer parameters
wafer_name = "CAP 104"
wafer_size = 4.000000
xsize = 2790.000000
ysize = 1950.000000
#xmax = 11
#ymax = 12
nchips = 104
nmodules = 2
init_chip = 2
end_chip = 3

real_origin_chip = "-11 -3"
origin_chip = "0 0" # normaly start with 0,0
home_chip = "-6 -12" # home (0um , 0um) could be different to origin (first die to measure)
flat_orientation = 0 # flat orientation: 0, 90, 180 or 270

# navigation options: 
# 1- UP-LEFT, UP-RIGHT, BOTTOM-LEFT, BOTTOM-RIGHT
# 2- BI (Bi-Directional movement), UNI (Uni-Directional movement)
# 3- ROW (Move by Row) or COLUMN (Move by Column)

#navigation_options = []
#navigation_options = np.append(navigation_options, ["UP-LEFT","BI","ROW"])
navigation_options = ["UPPER-LEFT","BI-DIRECTIONAL","ROW"]


# wafer positions
# wafer_positions = []
# wafer_positions = np.append(wafer_positions,["0 0","-3 0","-6 0","-9 0","-12 0"])
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
wafer_positions = ["0 0","-3 0","-6 0","-9 0","-12 0","-15 -4","-12 -4","-9 -4","-6 -4","-3 -4","0 -4","3 -4","6 -8","3 -8","0 -8","-3 -8","-6 -8","-9 -8","-12 -8","-15 -8","-18 -8","-18 -12","-15 -12","-12 -12","-9 -12","-6 -12","-3 -12","0 -12","3 -12","6 -12","9 -16","6 -16","3 -16","0 -16","-3 -16","-6 -16","-9 -16","-12 -16","-15 -16","-18 -16","-21 -16","-21 -20","-18 -20","-15 -20","-12 -20","-9 -20","-6 -20","-3 -20","0 -20","3 -20","6 -20","9 -20","9 -24","6 -24","3 -24","0 -24","-3 -24","-6 -24","-9 -24","-12 -24","-15 -24","-18 -24","-21 -24","-21 -28","-18 -28","-15 -28","-12 -28","-9 -28","-6 -28","-3 -28","0 -28","3 -28","6 -28","9 -28","6 -32","3 -32","0 -32","-3 -32","-6 -32","-9 -32","-12 -32","-15 -32","-18 -32","-18 -36","-15 -36","-12 -36","-9 -36","-6 -36","-3 -36","0 -36","3 -36","6 -36","3 -40","0 -40","-3 -40","-6 -40","-9 -40","-12 -40","-15 -40","-12 -44","-9 -44","-6 -44","-3 -44","0 -44"]


# distances from chip origin
wafer_modules = ["0.000000 0.000000","100.000000 0.000000"]
wafer_modules_name = ["0 0","100 0"]

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
"init_chip": init_chip,
"end_chip": end_chip,
"flat_orientation": flat_orientation,
"wafer_positions": wafer_positions,
"wafer_modules": wafer_modules,
"wafer_modules_name": wafer_modules_name,
"real_origin_chip": real_origin_chip,
"navigation_options": navigation_options

}







