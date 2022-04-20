#############################################################################################
#  FILE :  tenantFunctions.py                                                                #
#          Provides Tenant role supported functions                                          #
#          tenantPage()                                                                      #
#############################################################################################

import re
from Utils import confirm_ExitApplication
from dbOperations import createTenant, fetchTenantDetails

mobileNoRegex = r"^[0-9]+\b"
userFName =""
userLName=""
userMobileNo=""

def tenantPage(userName):
    error_entry = True
    signInSuccess = False
    while error_entry:
        print(" ****************  GREENCORP RENTALS  ****************")
        print(" ")
        print("Welcome {} !".format(userName))
        print("Apartment :--- name and unit number  ")
        print("Lease Term - ")
        print(" ")
        print("1. Dashboards")
        print("2. View Outstanding Payments If Any")
        print("3. Generate Payment invoice")
        print("4. Log Complaints")
        print("5. Sign out")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1:
                TenantDashboards(userName)
            elif optionSelected == 2:
                print("View Outstanding Payments If Any-- TO DO")
            elif optionSelected == 3:
                print("Generate Payment invoice-- TO DO")
            elif optionSelected == 4:
                print("Log Complaints -- TO DO")
            elif optionSelected == 5:
                error_entry = False
                quit()
            else:
                print("Wrong option Selected")
        except ValueError:
            continue
        else:
            wishtoContinue = confirm_ExitApplication()
            if wishtoContinue:
                continue
            else:
                error_entry = False
                quit()


def enterTenantDetails(userName):
    error_entry = True
    firstVisit = True

    global userFName, userLName, userMobileNo
    msg = " Submit Your Lease Agreement"
    print(" ****************  GREENCORP RENTALS  ****************")
    print(" ")
    print("Welcome {} !".format(userName))
    print(" ")

    while error_entry:
        print("1.{}".format(msg))
        print("2. Sign-Out")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1 and firstVisit:
                print("Please provide your profile information.")
                userFName = validateTenantFirstName()
                userLName = validateTenantLastName()
                userMobileNo = validateMobileNumber()

                print("Thank you for entering the details.\n")
                submit_entry = True
                while submit_entry:
                    wishtoSubmit = input("Are you sure to submit the Lease? Yes / No:")
                    if wishtoSubmit.upper() == "YES":
                        createTenant(userName,userFName,userLName,userMobileNo)
                        msg = "Dashboard"
                        firstVisit = False
                        submit_entry = False
                    elif wishtoSubmit.upper() == "NO":
                        submit_entry = False
                        firstVisit= True
                    else:
                        print("Wrong Option entered !. Please try again. ")
                        submit_entry = True
                        continue
            elif optionSelected == 2:
                quit()
            else:
                if firstVisit:
                    print("Wrong option Selected")
                    continue
                else:
                    displayDashboard(userName)

        except Exception:
            continue
        else:
            error_entry = True



def TenantDashboards(userName):
    print("************************  My Profile  ************************")
    fetchTenantDetails(userName)


def displayDashboard(userName):
    global userFName,userLName,userMobileNo
    print("************************  My Profile  ************************")
    print("Basic Information\n ")
    print("-------------------------------------------------------")
    print("\tFirst Name:{}".format(userFName))
    print("\tLast Name:{}".format(userLName))
    print("Contact Information\n ")
    print("-------------------------------------------------------")
    print("\tMobile Number:{}".format(userMobileNo))
    print("\tEmail ID:{}".format(userName))
    print("-------------------------------------------------------")


def validateTenantFirstName():
    check_Name = True

    while check_Name:
        try:
           userFirstName = input('Enter First Name:')
        except Exception:
            continue
        else:
            check_Name = False
    return userFirstName


def validateTenantLastName():
    check_Name = True

    while check_Name:
        try:
           userLastName  = input('Enter Last Name:')
        except Exception:
            continue
        else:
            check_Name = False
    return userLastName


def validateMobileNumber():
    check_mobileNo = True
    mobileNo = input('Enter your Mobile Number:')
    while check_mobileNo:
        match = re.fullmatch(mobileNoRegex, mobileNo)
        try:
            if match is None:
                print("Mobile number should only contain numeric. Please provide a valid one.\n")
                mobileNo = input('Enter your Mobile Number:')
                continue
        except Exception:
            continue
        else:
            check_mobileNo = False
    return mobileNo



