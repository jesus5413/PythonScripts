import sys
import re
import difflib

# getAddress
#
# Parameters
#   file - A pointer that points to the last point area of the file
#
# returns
#   returns a dictionary that contains the address of the customer
#
# Purpose
#   - To parse the file and store tha appropriate address and returns the address with in a dictionary


def getAddress (file):
    address = {'LINES': "", 'CITY': "", 'STATE': "", 'ZIP': ""}

    while True:  # traverses through the file
        inputine = file.readline()
        inputine = inputine.rstrip('\n')
        if inputine.find("ADDREND") == 0 or inputine.find(""):
            return address

        if inputine.find("LINE") == 0:  # Checks for lines
            if len(address['LINES']) >= 1:  # checls for the len of of elements in lines
                address['LINES'] = address['LINES'] + " " + inputine.split(' ', 1)[1]
            else:
                address['LINES'] = inputine.split(' ', 1)[1]

        if inputine.find("CITY") == 0:  # checks for citys
            address['CITY'] = inputine.split(' ', 1)[1]

        if inputine.find("STATE") == 0:  # checks for state
            address['STATE'] = inputine.split(' ', 1)[1]

        if inputine.find("ZIP") == 0:  # checks for zzip
            address['ZIP'] = inputine.split(' ', 1)[1]


# printAddress
#
# Parameters
#   addressD - a dictionary containing an address
#   addressNr - the nth address associated with the customer
# returns
#   n/a - just prints the address
#
# Purpose
#   - to print the address of the customer
def printAddress (addressD, addressNr):
    print("%d    %s"%(addressNr, addressD['LINES']))
    print("     %s,  %s %s \n"%(addressD['CITY'], addressD['STATE'], addressD['ZIP']))












