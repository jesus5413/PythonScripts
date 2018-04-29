#! /usr/bin/python

import sys
import address as adr
import checkAddress as bdr
import pprint


# Purpose:
#   - Script get a file from the command line and outputs the name and the addresses associated with the name
#
#
# Input:
# CUSTOMER BOB WIRE
# ADDRBEG
# LINE 123 DIRT
# LINE RD
# CITY SAN ANTONIO
# STATE TX
# ZIP 78210
# ADDREND
# ADDRBEG
# LINE 123 DIRT
# CITY SAN ANTONIO
# STATE TX
# ZIP 78210
# ADDREND
# ADDRBEG
# LINE 123 DIRT LN
# CITY SAN ANTONIO
# STATE TX
# ZIP 78210
# ADDREND
# CUSTOMEREND
#
# Output:
#  BOB WIRE
# 1    123 DIRT RD
#      SAN ANTONIO,  TX 78210
#
# 2    123 DIRT
#      SAN ANTONIO,  TX 78210
#
# 3    123 DIRT LN
#      SAN ANTONIO,  TX 78210

if len(sys.argv) < 2:
    print("filename needed!")
    sys.exit()

file = open(sys.argv[1], "r")
a = []
counter = 1
# loop to traverse through the file
while True:

    inputLine = file.readline()  # gets the next lien
    if inputLine == "":  # checks for end of file
        break
    inputLine = inputLine.rstrip('\n')  # removes the new line so there wont be an empty line

    #  gets the customer name and removes the word customer from the line
    if inputLine.find("CUSTOMER") == 0 and inputLine.find("CUSTOMEREND") == -1:
        if a is not None:
            bdr.scoring(a)
        a = []
        counter = 1
        print("\n")
        print("%-50s %-15s %-15s %-15s %-15s %-15s \n"%(inputLine.split(' ', 1)[1], "StNum", "Direction", "AptNum", "StType", "StName"))
    if inputLine.find("ADDRBEG") == 0:
        test = adr.getAddress(file)
        adr.printAddress(test, counter)
        addTest = bdr.parseAddress(test, counter)
        counter += 1
        stringT = "some string"
        if addTest is None:
            print("---------------------------------------There was an error")
        else:
            finalTest = bdr.addressSyntaxException(addTest)
            if finalTest["Compare"] is True:
                a.append(finalTest)
bdr.scoring(a)
file.close()
