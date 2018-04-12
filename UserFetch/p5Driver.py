#! /usr/bin/python

import sys
import address as adr


if len(sys.argv) < 2:
    print("filename needed!")
    sys.exit()

file = open(sys.argv[1], "r")

counter = 1
# loop to traverse through the file
while True:

    inputLine = file.readline()  # gets the next lien
    if inputLine == "":  # checks for end of file
        break
    inputLine = inputLine.rstrip('\n')  # removes the new line so there wont be an empty line

    #  gets the customer name and removes the word customer from the line
    if inputLine.find("CUSTOMER") == 0 and inputLine.find("CUSTOMEREND") == -1:
        counter = 1
        print(inputLine.split(' ', 1)[1])

    if inputLine.find("ADDRBEG") == 0:
        test = adr.getAddress(file)
        adr.printAddress(test, counter)
        counter += 1

file.close()
