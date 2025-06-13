# Program constants
version = 'v6.0 - Beta 2'

# BBDD connection
mysqlhost = "localhost"
mysqluser = "root"
mysqlpassword = "Mysql123" # Mysql123 or blank in cnm
mysqldatabase = "labs_new" # labs_new or labs in cnm


# this after login
if 'username' not in globals():
	username = "default"

# directory base & others
base_dir = "/config/" + username + "/"
instruments_dir = "instruments"
tests_dir = "tests"
probers_dir = "probers"
wafermaps_dir = "wafermaps"
results_dir = "results"
reports_dir = "reports"

# files to save
plot_file = "lecturas.txt"
process_file = "process.txt"
import_report_file = "report_import.txt"

# globals variables
counter = 0
errorLogin = False
username = ""
password = ""
connection = ""
user_id_db = 0
username_db = ""
email_db = ""

# status variables system
cartographic_measurement = False

# default values
txtprocess = "K6H316-08P1-TEST1"
txtlot = "K6H316"
txtwafer = "08P1"
txtmask = "LINDA"
txttemperature = "26"
txthumidity = "48"







