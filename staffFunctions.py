#############################################################################################
#  FILE :  staffFunctions.py                                                                #
#          Provides Staff role supported functions                                          #
#          staffPage()                                                                      #
#############################################################################################

import sqlite3
import datetime
import calendar
import pandas as pd
from tabulate import tabulate
from colorama import init
from termcolor import colored

from Utils import confirm_ExitApplication

connection = sqlite3.connect("Greencorp.db")


def staffPage(userName):
    error_entry = True
    signInSuccess = False
    while error_entry:
        print(" ****************  GREENCORP RENTALS  ****************")
        print(" ")
        print("Welcome {} !".format(userName))
        print("1. View apartment status")
        print("2. Approve Tenant Profile")
        print("3. Confirm Apartment Tour Request")
        print("4. Generate Booking")
        print("5. Contract Termination")
        print("6. Sign out")
        try:
            optionSelected = int(input("Choose Your Option(?): "))
            if optionSelected == 1:
                print("TO DO")
            elif optionSelected == 2:
                print("TO DO")
            elif optionSelected == 3:
                print("Confirm Apartment Tour Request -- TO DO")
            elif optionSelected == 4:
                generate_booking(userName)
            elif optionSelected == 5:
                booking_termination()
            elif optionSelected == 6:
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


def booking_termination():
    print("Please enter the booking details:")
    BookingID = (input("Booking ID : "))
    bookingnumber = booking_exists(BookingID)
    if bookingnumber == '':
        print("Please enter valid booking ID!\n")
    else:
        terminate_confirmation = input("Are you sure, you want to terminate the booking "+bookingnumber+" (Yes/No) : ")
        if terminate_confirmation.upper() == 'YES':
            cursor = connection.cursor()
            query_terminate = "UPDATE BOOKING SET BOOKINGSTATUS = ? WHERE BOOKINGID = ?"
            parameters_terminate = ('Terminated', BookingID)
            cursor.execute(query_terminate, parameters_terminate)
            connection.commit()
            print("Booking", bookingnumber, " terminated successfully!\n")


def generate_booking(userName):
    print("Please enter the booking details:")
    BookingID = (input("Booking ID : "))
    UnitID = (input("Unit ID : "))
    TenantID = (input("Tenant ID : "))
    TenancyStartDate = (input("Tenancy Start Date(Format : YYYY-MM-DD) : "))
    TenancyEndDate = (input("Tenancy End Date(Format : YYYY-MM-DD) : "))
    Rentpermonth = int(input("Rent per month after discount : "))
    Noofdays = datetime.datetime.strptime(TenancyEndDate, '%Y-%m-%d') - datetime.datetime.strptime(TenancyStartDate, '%Y-%m-%d')
    if BookingID == "" or UnitID == "" or TenantID == "" or TenancyStartDate == "" or TenancyEndDate == "" or Rentpermonth == "":
        print("Please enter the relevant booking details and proceed!")
        generate_booking(userName)
    else:
        tenantexistance = tenant_exists(TenantID)
        unitexistance = Unit_exists(UnitID)
    if tenantexistance == 0:
        print("Please enter valid tenant ID!\n")
        generate_booking(userName)
    elif unitexistance == 0:
        print("Please enter valid unit ID!\n")
        generate_booking(userName)
    elif int(Noofdays.days) < 364:
        print("Please enter a valid Tenancy End Date(Duration of tenancy period should be one year)!!\n")
        generate_booking(userName)
    else:
        Totalleaseprice = 12*Rentpermonth
        cursor = connection.cursor()
        query = "INSERT INTO BOOKING (BOOKINGID,UNITID,TENANTID, NOOFINSTALMENTS, TENANCYSTARTDATE, TENANCYENDDATE, SECURITYDEPOSIT, RENTPERMONTH, TOTALLEASEPRICE, BOOKINGSTATUS, LEASEADVISORID) VALUES(?,?,?,?,?,?,?,?,?,?,?);"
        parameters = (BookingID, UnitID, TenantID, 12, TenancyStartDate, TenancyEndDate, Rentpermonth, Rentpermonth, Totalleaseprice, 'Booked', userName)
        cursor.execute(query, parameters)
        connection.commit()
        print(colored("-----------------------------------------------------------------", 'blue'))
        print(colored("Booking generated successfully! Please find below booking details", 'blue'))
        print(colored("\n Booking Details:", 'green'))
        print(colored("***********************************", 'green'))
        print(colored("Booking ID :" + BookingID, 'blue'))
        print(colored("Unit :" + UnitID, 'blue'))
        print(colored("Tenant Name :" + tenantdetails(TenantID), 'blue'))
        print(colored("Number of instalments : 12", 'blue'))
        print(colored("Total Lease Price :" + str(Totalleaseprice), 'blue'))
        print(colored("\n Payment Plan Item Details:", 'green'))
        print(colored("***********************************", 'green'))
        for i in range(12):
            PPIdate = datetime.datetime.strptime(TenancyStartDate, '%Y-%m-%d')
            InstalmentDate = add_months(datetime.date(PPIdate.year, PPIdate.month, PPIdate.day), i)
            query1 = "INSERT INTO PAYMENTPLANITEMS (BOOKINGID,TENANTID, DUEDATE, INSTALMENTNUMBER, INSTALMENTAMOUNT, UNITID) VALUES(?,?,?,?,?,?);"
            parameters1 = (BookingID, TenantID, InstalmentDate, i + 1, Rentpermonth, UnitID)
            cursor.execute(query1, parameters1)
            connection.commit()
        query_update = "UPDATE UNIT SET UNITSTATUS = ? WHERE UNITNUMBER = ?"
        parameters_update = ('Leased', UnitID)
        cursor.execute(query_update, parameters_update)
        connection.commit()
        query2 ="SELECT PAYMENTPLANITEMID, DUEDATE, INSTALMENTNUMBER, INSTALMENTAMOUNT FROM PAYMENTPLANITEMS WHERE BOOKINGID = ?"
        execute = cursor.execute(query2, (BookingID,))
        df = pd.DataFrame(cursor.fetchall(), columns=['PAYMENTPLANITEMID', 'DUEDATE', 'INSTALMENTNUMBER', 'INSTALMENTAMOUNT'])
        print(colored(tabulate(df, headers='keys', tablefmt='psql'), 'blue'))
        cursor.close()


def tenant_exists (Tenantid):
    User_id = ''
    cursor = connection.cursor()
    query = "SELECT TENANTID FROM TENANT WHERE TENANTID = ?"
    execute = cursor.execute(query, (Tenantid,))
    records = cursor.fetchall()
    for row in records:
        User_id = row[0]
    if User_id == Tenantid:
        return 1
    else:
        return 0


def Unit_exists (Unitid):
    Unitnumber = ''
    cursor = connection.cursor()
    query = "SELECT UNITNUMBER FROM UNIT WHERE UNITNUMBER = ?"
    execute = cursor.execute(query, (Unitid,))
    records = cursor.fetchall()
    for row in records:
        Unitnumber = row[0]
    if Unitnumber == Unitid:
        return 1
    else:
        return 0


def tenantdetails(TenantID):
    tenant = ''
    cursor = connection.cursor()
    query = "SELECT FIRSTNAME,MIDDLENAME,LASTNAME FROM TENANT WHERE TENANTID = ?"
    execute = cursor.execute(query, (TenantID,))
    records = cursor.fetchall()
    for row in records:
        if row[0] != None:
            tenant = str(row[0])
        if row[1] != None:
            tenant += " " + str(row[1])
        if row[2] != None:
            tenant += " " + str(row[2])
    return tenant

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

def booking_exists(BookingID):
    Bookingnumber = ''
    cursor = connection.cursor()
    query = "SELECT BOOKINGID FROM BOOKING WHERE BOOKINGID = ?"
    execute = cursor.execute(query, (BookingID,))
    records = cursor.fetchall()
    for row in records:
        Bookingnumber = row[0]
    if Bookingnumber == BookingID:
        return Bookingnumber
    else:
        return ''


staffPage('ben@greencorp.com')