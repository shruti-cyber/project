#######################################################################################################
#  FILE :  dbOperations.py                                                                          #
#          Provides backend related functions                                                       #
#          apartmentSearchList() , bookAppointment(), createStaffAccount(), viewApartmentStatus()   #
#          addNewProperty()                                                                         #
#######################################################################################################

import re
import sqlite3
from prettytable import PrettyTable
from tabulate import tabulate

from Utils import confirm_ExitApplication

connection = sqlite3.connect("Greencorp.db")

uNameRegex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
PropertyName = ''
Location = ''
locationInp = ''


def apartmentSearchList():
    global PropertyID, locationInp, PropertyName, Location, UnitNumber, Type, RentperMonth, NoofBedrooms, TotalArea, NoofBathrooms
    check_loc = True
    print("***********************************************************************************")
    print("     Greencorp Rentals has properties across Kitchener, Waterloo and Cambridge ")
    print("-----------------------------------------------------------------------------------")
    while check_loc:
        try:
            locList = ["kitchener", "waterloo", "cambridge"]
            input1 = input("Enter your preferred location : ")
            locationInp = input1.lower()
            if locationInp not in locList:
                print("Please enter a valid location!")
                continue
            else:
                check_loc = False
        except ValueError:
            continue
        else:
            check_Name = False

    cursor = connection.cursor()
    query1 = "SELECT PropertyName " \
             "FROM UNIT WHERE UnitStatus = 'Available' AND Location = '{}'; ".format(locationInp)
    cursor.execute(query1)
    results1 = cursor.fetchall()
    PropertyName = str(results1)
    query2 = "SELECT UnitNumber, Type, RentperMonth, NoofBedrooms, NoofBathrooms, TotalArea " \
             "FROM UNIT WHERE UnitStatus = 'Available' AND Location = '{}'; ".format(locationInp)
    cursor.execute(query2)
    results2 = cursor.fetchall()
    cursor.close()
    if len(results2) > 0:
        print(" ")
        print("      {}       {}      ".format(results1[0][0], locationInp))
        print("-------------------------------------------------------------------------------")
        print(tabulate(results2,
                       headers=['UnitNumber', 'Type', 'Rent Per Month', 'Bedrooms', 'Bathrooms', 'TotalArea'],
                       tablefmt='simple'))
        print(" ")
        print("Please book an appointment with our staff for a tour and other details!")
        print(" ")


def bookAppointment():
    print("******************************************************")
    print("      Book an appointment with our staff here")
    print("-------------------------------------------------------")
    success = True
    while success:
        try:
            fname = input(" First Name   : ")
            lname = input(" Last Name    : ")
            email = input(" Email ID     : ")
            matchSyntax = re.fullmatch(uNameRegex, email)
            if matchSyntax is None:
                print("Email {} is invalid. Please provide a valid one.\n".format(email))
                email = input(" Email ID     : ")
            phone = input(" Phone Number : ")
        except ValueError:
            continue
        else:
            check_Name = False
    return True


def createStaffAccount():
    fname = ''
    lname = ''
    email = ''
    print("******************************************************")
    print("      Create Staff Account here")
    print("-------------------------------------------------------")
    success = True
    while success:
        try:
            fname = input(" First Name   : ")
            lname = input(" Last Name    : ")
        except ValueError:
            continue
        else:
            check_Name = False
            email = fname + lname + '@greencorp.com'
            newPassword = fname
            UserType = "Staff"
            cursor = connection.cursor()
            query = "insert into USER (UserType, Username, Password) values ('{}','{}','{}');".format(UserType, email,
                                                                                                      newPassword)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            cursor.close()
            print(" Staff Account Created Successfully !")
        return True


def viewApartmentStatus():
    status = ''
    location = ''
    print("******************************************************")
    print("                GREENCORP RENTALS                     ")
    print("------------------------------------------------------")
    print(" ")
    error_entry = True
    while error_entry:
        print(" 1. Available Units ")
        print(" 2. Leased Units ")
        print(" 3. Return to main page")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1:
                status = "Available"
                unitStatusQueryFunction(status)
            elif optionSelected == 2:
                status = "Leased"
                unitStatusQueryFunction(status)
            elif optionSelected == 3:
                return False
            else:
                print("Wrong option Selected")
                continue
        except ValueError:
            continue
        else:
            error_entry = True
           # wishtoContinue = confirm_ExitApplication()
           # if wishtoContinue:
           #     error_entry = True
           #     continue
            #else:
            #    error_entry = False


def unitStatusQueryFunction(status):
    check_loc = True
    while check_loc:
        try:
            locList = ["kitchener", "waterloo", "cambridge"]
            input1 = input("Enter Property location : ")
            if input1.lower() not in locList:
                print("Please enter a valid location!")
                continue
            else:
                check_loc = False
                location = input1.lower()
        except ValueError:
            continue
        else:
            check_loc = False

    cursor = connection.cursor()
    query = "SELECT UnitNumber, Type " \
            "FROM UNIT WHERE UnitStatus = ? AND Location = ?;"
    cursor.execute(query, (status, location))
    results = cursor.fetchall()
    cursor.close()
    if len(results) > 0:
        print(" ")
        print("      {}       {}      ".format(results[0][0], locationInp))
        print("-------------------------------------------------------------------------------")
        print(tabulate(results, headers=['UnitNumber', 'Type'], tablefmt='simple'))
        print(" ")
        return True
    else:
        print("No Units present for the selected option !")
        return False


def fetchTenantDetails(userName):
    cursor = connection.cursor()
    query1 = "SELECT FirstName, LastName, EmailID, ContactNumber FROM Tenant WHERE EmailID='{}';".format(userName)
    cursor.execute(query1)
    results = cursor.fetchall()
    if len(results) > 0:

        print(tabulate(results, headers=['FirstName', 'LastName', 'EmailID', 'ContactNumber'], tablefmt='simple'))
        print("---------------------------------------------------------------")


def addNewProperty():
    propertyIDTemp = ''
    str1 = ''
    print("******************************************************")
    print("      Add New Property Details here")
    print("-------------------------------------------------------")
    success = True
    while success:
        try:
            projectID = input("Project ID       : ")
            projectName = input("Project Name     : ")
            projectLocation = input("Project Location :")
        except ValueError:
            continue
        else:
            success = False
            cursor = connection.cursor()
            query1 = "SELECT PropertyID FROM Property ORDER BY PropertyID DESC LIMIT 1"
            cursor.execute(query1)
            results = cursor.fetchall()
            for result in results:
                propID = result[0]

            idNum = int(propID.split('-')[1]) + 1
            propertyID = "PROP-" + str(idNum)
            query = "insert into Property (PropertyID, ProjectID, PropertyName, Location) values ('{}','{}','{}','{}');" \
                .format(propertyID, projectID, projectName, projectLocation)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            cursor.close()
            print(" Property Details Added/Created Successfully !")
        return True


def approveTenantProfile():
    propertyIDTemp = ''
    str1 = ''
    print("******************************************************")
    print("      Approve Tenant Profile Page")
    print("-------------------------------------------------------")

    cursor = connection.cursor()
    query = "SELECT UserName FROM User WHERE UserType = '{}';".format("User")
    cursor.execute(query)
    userresults = cursor.fetchall()
    #cursor.close()
    if len(userresults) > 0:
        print(" ")
        print(tabulate(userresults, headers=['Profiles To Approve'], tablefmt='simple'))
        print(" ")
    else:
        print("No Pending Approvals !")
        return False

    userList = []
    for name in userresults:
        userList.append(str(name[0]))

    success = True
    while success:
        try:
            userNameToApprove = input("Enter the Tenant Name for approval       : ")
            if userNameToApprove.lower() not in userList:
                print("Please enter a valid Tenant Name!")
                continue
        except ValueError:
            continue
        else:
            query = "UPDATE User SET UserType='{}' WHERE Username='{}';".format("NewTenant",userNameToApprove)
            cursor.execute(query)
            cursor.execute("COMMIT;")
            cursor.close()
            print(" Tenant profile {} is Approved !".format(userNameToApprove))
            success = False
    return True


# Function to create a new Tenant
def createTenant(userName, tFname, tLname, tContactNo):
    cursor = connection.cursor()
    #Fetch Last Added TenantID
    query1 = "SELECT TenantID FROM Tenant ORDER BY TenantID DESC LIMIT 1"
    cursor.execute(query1)
    results = cursor.fetchall()
    tempID = str(results[0][0])

    idNum = int(tempID[1:len(tempID)]) + 1
    newTenantID = "T" + str(idNum)

    #Query to Add Tenant into Tenant table
    query = "insert into Tenant (TenantID, TenantType, FirstName, LastName, EmailID, ContactNumber) values ('{}','{}','{}','{}','{}','{}');".format(newTenantID,"Tenant",tFname, tLname, userName,tContactNo)
    cursor.execute(query)
    cursor.execute("COMMIT;")
    print(" Tenant Account Created Successfully !")

    #change UserType in USER table to Tenant
    query = "UPDATE User SET UserType='{}' WHERE Username='{}';".format("Tenant", userName)
    cursor.execute(query)
    cursor.execute("COMMIT;")
    cursor.close()
    return True
