global contact_test, contact_errors, test_status, actual_height

# CONTACT PROGRAM : contact_test variable
# -1 : first die, init program
# return 0: not contact
# return 1: some in contact but not all (be carefull)
# return 2: all in contact
# return 3: abort test

max_contact_errors = 3


# contact_test = -1 (beggining)
# FIRST DIE (INIT)
if str(dieActual)=="1" and str(moduleActual)=="1" and contact_test==-1:
	contact_errors = 0


# -----------
# TESTING DIE
# -----------

#wait = input("Press Enter to continue.")

	
contact_test = -1

# if float(actual_height)>=37500:
# 	contact_test = 0
# if float(actual_height)>=37750:
# 	contact_test = 1
# if float(actual_height)>=37850:
# 	contact_test = 2


if contact_test==-1:
	contact_test = 3


if contact_test==3:
	contact_errors = contact_errors + 1	

print("Die actual: " + str(dieActual) + ", module actual: " + str(moduleActual))
print("- Actual height: " + str(actual_height))
print("- Contact test: " + str(contact_test))

if contact_errors==max_contact_errors:
	print("Test aborted for max contact errors: "+str(max_contact_errors))
	test_status.status = "ABORTED"

