import sys
import re


def getAddress (file):
    address = {'LINES': "", 'CITY': "", 'STATE': "", 'ZIP': ""}

    while True:
        inputine = file.readline()
        inputine = inputine.rstrip('\n')
        if inputine.find("ADDREND") == 0 or inputine.find(""):
            return address

        if inputine.find("LINE") == 0:
            if len(address['LINES']) >= 1:
                address['LINES'] = address['LINES'] + " " + inputine.split(' ', 1)[1]
            else:
                address['LINES'] = inputine.split(' ', 1)[1]

        if inputine.find("CITY") == 0:
            address['CITY'] = inputine.split(' ', 1)[1]

        if inputine.find("STATE") == 0:
            address['STATE'] = inputine.split(' ', 1)[1]

        if inputine.find("ZIP") == 0:
            address['ZIP'] = inputine.split(' ', 1)[1]


def printAddress (addressD, addressNr):
    print("%d    %s"%(addressNr, addressD['LINES']))
    print("     %s,  %s %s \n"%(addressD['CITY'], addressD['STATE'], addressD['ZIP']))
