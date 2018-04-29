import sys
import re
import difflib

# parseAddress
#
# Parameters
#   info - A dictionary filled with address info
#   counter - The number that represents the address index
#
# returns
#   returns a dictionary that contains a parsed address
#
# Purpose
#   - To parse an address in appropriate sections
def parseAddress(info, counter):
    mainAddress = {'StreetNum': "",
                   'StreetType': "",
                   'Direction': "",
                   'AptNum': "",
                   'City': "",
                   'State': "",
                   'StrName': "",
                   'Zip': "",
                   'AdrLine': "",
                   'Compare': True,
                   'Counter': ""}

    mainAddress['City'] = info['CITY']
    mainAddress['State'] = info['STATE']
    mainAddress['Zip'] = info['ZIP']
    mainAddress['AdrLine'] = info['LINES']
    mainAddress['Counter'] = counter
    adrParse = info['LINES'].split()
    oldNum = adrParse[0]
    newNum = oldNum.replace("-","")
    mainAddress['StreetNum'] = newNum
    adrParse.pop(0)

    if len(adrParse) == 3:
        adrParse, mainAddress['Direction'] = addressChecker(adrParse)

    if len(adrParse) == 1:
        strName = ' '.join(adrParse).upper();
        newStrName = strName.replace(".", "")
        mainAddress["StrName"] = newStrName
        return mainAddress

    adrParse, mainAddress['AptNum'] = getAptNumber(adrParse)

    if len(adrParse) == 1:
        strName = ' '.join(adrParse).upper();
        newStrName = strName.replace(".", "")
        mainAddress["StrName"] = newStrName
        return mainAddress

    adrParse, mainAddress['StreetType'] = getStreetType(adrParse)

    if len(adrParse) == 1:
        strName = ' '.join(adrParse).upper();
        newStrName = strName.replace(".", "")
        mainAddress["StrName"] = newStrName
        return mainAddress

    adrParse, mainAddress['Direction'] = getDirection(adrParse)

    if len(adrParse) >= 1:
        strName = ' '.join(adrParse).upper();
        newStrName = strName.replace(".", "")
        mainAddress["StrName"] = newStrName
        return mainAddress

    return mainAddress;

# addressSyntaxException
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#   returns a dictionary that contains a parsed address
#
# Purpose
#   - To raise Exception errors and as well decide which dictionaries to throw out
def addressSyntaxException(info):
    address = info['StreetNum']
    adrNum = address[0]
    if not info['AdrLine']:
        print("                                                               ************* Address does not exist *************")
        info["Compare"] = False
        return info
    if not info['City']:
        print("                                                               *************** There is no City ******************")
        info['Compare'] = False
        return info
    if not info['State']:
        print("                                                                *************** There is no state ****************")
        info['Compare'] = False
        return info
    if not info['Zip'] or len(info['Zip']) < 5 or re.search('[a-zA-Z]', info['Zip']):
        print("                                                                *************** Zip code Syntax Error *******************")
        info['Compare'] = False
        return info
    if not info['StreetNum'] or not adrNum.isdecimal():
        print("                                                                **************** Error with StreetNum ************")
        info['Compare'] = False
        return info

    print("%55s %18s %15s %15s %20s\n"
          % (info['StreetNum'], info['Direction'], info['AptNum'], info['StreetType'], info['StrName']))

    return info


# streetType
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#   returns a street type
#
# Purpose
#   - To decide which street type the address has
def streetType(info):
    #standard types of street acronyms
    strType = {          "avenue":
                         ["av", "ave", "aven", "avenu",
                          "avn", "avnue", "avenue", "ave."],
                         "boulevard":
                         ["blvd", "blvd.", "boul", "boulevard", "boulv"],
                         "circle":
                         ["cir", "circ", "circl", "crcl", "crcle", "circle"],
                         "height":
                         ["ht", "height"],
                         "lane":
                         ["ln", "lane"],
                         "ridge":
                         ["rdg", "rdge", "ridge"],
                         "road":
                         ["rd", "road", "rd."],
                         "route":
                         ["rte", "route"],
                         "run":
                         ["run"],
                         "springs":
                         ["spgs", "spngs", "sprngs", "springs"],
                         "square":
                         ["square", "sq", "sq."],
                         "street":
                         ["strt", "st", "str", "street", "st."],
                         "trail":
                         ["trl", "trail"],
                         "terrace":
                         ["ter", "terr", "terrace"],
                         "valley":
                         ["vally", "vlly", "vly", "valley"],
                         "view":
                         ["vw", "view"],
                         "way":
                         ["wy", "way"]
            }

    for key in strType.keys():
        for value in strType[key]:
            if ''.join(sorted(info.lower())) == ''.join(sorted(value)):
                return key.upper()

    return ""

# getTtreetType
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#   returns a street type and a popped list
#
# Purpose
#   - To decide which street type the address has and to minimize the parsed address
def getStreetType(parsedAddress):

    realStrType = ""
    for key in parsedAddress:
        strType = streetType(key)
        if strType != "":
            realStrType = strType.upper()
            i = parsedAddress.index(key)
            parsedAddress.pop(i)

    return parsedAddress, realStrType

# direction
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#   returns a direction type
#
# Purpose
#   - To decide which direction the address has
def direction(info):

    direction = {             "east":
                              ["e", "east", "e."],
                              "north":
                              ["n", "north", "n."],
                              "northeast":
                              ["ne", "n east", "north e", "northeast",
                               "north east"],
                              "northwest":
                              ["nw", "n west", "north w", "northwest",
                               "north west"],
                              "northsouth":
                              ["ns", "n south", "north s", "northsouth",
                               "north south"],
                              "south":
                              ["s", "south"],
                              "southeast":
                              ["se", "s east", "southeast"],
                              "southwest":
                              ["sw", "s west", "southwest", "s.w."],
                              "west":
                              ["w", "west", "w."]
                }

    for key in direction.keys():
        for value in direction[key]:
            if ''.join(value) == ''.join(info.lower()):
                return key.upper()

    return ""

# getDirection
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#   returns a direction type and a minimized parsed address
#
# Purpose
#   - To decide which direction the address has
def getDirection(parsedAddress):
    strDir = []
    tempPopList = []
    counter = 0
    tempStr = ""
    for key in parsedAddress:
        i = parsedAddress.index(key)
        temp = direction(key)

        if temp != "":
            if (i + 1) < len(parsedAddress):
                checker = parsedAddress[(i + 1)]

                if direction(checker) != "":
                    if len(parsedAddress) >= 5:
                        strDir.append(key)
                        tempPopList.append(i)
                    continue
            strDir.append(temp)
            tempPopList.append(i)

    strString = ' '.join(strDir).lower()
    strString = direction(strString)
    tempPopList.reverse()

    for k in tempPopList:
        parsedAddress.pop(k)

    return parsedAddress, strString


# getAptNumber
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#   returns an apt number and a minimized parsed address
#
# Purpose
#   - To check if it has an apt number and return that number
def getAptNumber(parsedAddress):

    aptList = ["apartment", "apt", "nr", "#"]
    aptNmb = ""

    checker = False  # to get aptNmb

    for key in parsedAddress:
        if key.startswith("#"):

            if len(key) > 1:

                aptNmb = re.sub(r'\W', '', key)  # to get the apt number

                parsedAddress.pop(parsedAddress.index(key))
                break

            else:
                checker = True

        elif key.lower() in aptList:
            checker = True

        elif checker is True and key.lower() not in aptList:
            aptNmb = parsedAddress.pop(parsedAddress.index(key))
            break

    for key in aptList:
        for key2 in parsedAddress:
            if key2.lower() == key.lower():
                parsedAddress.remove(key2)

    return parsedAddress, aptNmb


# addressChecker
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#   returns a direction type and a minimized parsed address for addresses that are less than 3
#
# Purpose
#   - To decide which direction the address has
def addressChecker(parsedAddress):

    strDir = []
    tempPopList = []
    counter = 0
    tempStr = ""
    for key in parsedAddress:
        i = parsedAddress.index(key)
        temp = direction(key)

        if temp != "":
            if (i + 1) < len(parsedAddress):
                checker = parsedAddress[(i + 1)]

                if direction(checker) != "":
                    checker2 = parsedAddress[(i+2)]
                    if direction(checker2) == "":
                        strDir.append(key)
                        tempPopList.append(i)
                        break
            try:
                checker3 = parsedAddress[(i+2)]
                if direction(checker3) != "":
                    strDir.append(checker3)
                    tempPopList.append(parsedAddress.index(checker3))
                    break
            except IndexError:
                strDir.append(temp)
                tempPopList.append(i)

    strString = ' '.join(strDir).lower()
    strString = direction(strString)
    tempPopList.reverse()

    for k in tempPopList:
        parsedAddress.pop(k)

    return parsedAddress, strString


# scoring
#
# Parameters
#   info - A dictionary filled with address info
#
#
# returns
#
#
# Purpose
#   - To score similarities between addresses and print out that information
def scoring(infoList):
    print("%10s  %10s  %10s"%("Address", "Address","Score"))
    for key in infoList:
        for key2 in infoList:
            score = 0
            if key2['Compare'] == False:
                continue
            if key == key2:
                key2['Compare'] = False
                continue


            if (key['StreetNum'] and key2['StreetNum']) and (key['StreetNum'] == key2['StreetNum']):
                score += 20
            elif (key['StreetNum'] and key2['StreetNum']) and key['StreetNum'] != key2['StreetNum']:
                score -= 20
            elif not key['StreetNum'] and not key2['StreetNum']:
                score += 0
            elif (not key['StreetNum'] and key2['StreetNum']) or (key['StreetNum'] and not key2['StreetNum']):
                score -= 20



            if key['StreetType'] and key2['StreetType'] and key['StreetType'] == key2['StreetType']:
                score += 10
            elif key['StreetType'] and key2['StreetType'] and key['StreetType'] != key2['StreetType']:
                score -= 10
            elif not key['StreetType'] and not key2['StreetType']:
                score += 10
            elif (not key['StreetType']and key2['StreetType']) or (key['StreetType'] and not key2['StreetType']):
                score += 5




            if key['Direction'] and key2['Direction'] and key['Direction'] == key2['Direction']:
                score += 5
            elif key['Direction'] and key2['Direction'] and key['Direction'] != key2['Direction']:
                score -= 10
            elif not key['Direction'] and not key2['Direction']:
                score += 5
            elif (not key['Direction']and key2['Direction']) or (key['Direction'] and not key2['Direction']):
                score -= 5




            if key['AptNum'] and key2['AptNum'] and key['AptNum'] == key2['AptNum']:
                score += 20
            elif key['AptNum'] and key2['AptNum'] and key['AptNum'] != key2['AptNum']:
                sqe = difflib.SequenceMatcher(None, key['AptNum'], key2['AptNum'])
                if sqe.ratio() > 0.6:
                    squScore = 5 * sqe.ratio()
                    score += squScore
                else:
                    score -= 20
            elif not key['AptNum'] and not key2['AptNum']:
                score += 10
            elif (not key['AptNum']and key2['AptNum']) or (key['AptNum'] and not key2['AptNum']):
                score -= 10





            if key['City'] and key2['City'] and key['City'] == key2['City']:
                score += 20
            elif key['City'] and key2['City'] and key['City'] != key2['City']:
                sqe = difflib.SequenceMatcher(None, key['City'], key2['City'])
                if sqe.ratio() > 0.6:
                    squScore = 15 * sqe.ratio()
                    score += squScore
                else:
                    score -= 20
            elif not key['City'] and not key2['City']:
                score += 10
            elif (not key['City']and key2['City']) or (key['City'] and not key2['City']):
                score -= 10




            if key['State'] and key2['State'] and key['State'] == key2['State']:
                score += 10
            elif key['State'] and key2['State'] and key['State'] != key2['State']:
                score -= 20
            elif not key['State'] and not key2['State']:
                score += 0
            elif (not key['State']and key2['State']) or (key['State'] and not key2['State']):
                score -= 0


            if key['StrName'] and key2['StrName'] and key['StrName'] == key2['StrName']:
                score += 20
            elif key['StrName'] and key2['StrName'] and key['StrName'] != key2['StrName']:
                sqe = difflib.SequenceMatcher(None, key['StrName'], key2['StrName'])
                if sqe.ratio() > 0.6:
                    squScore = 10 * sqe.ratio()
                    score += squScore
                else:
                    score -= 5
            elif not key['StrName'] and not key2['StrName']:
                score -= 20
            elif (not key['StrName']and key2['StrName']) or (key['StrName'] and not key2['StrName']):
                score -= 20


            if key['Zip'] and key2['Zip'] and len(key['Zip']) == 10 and len(key2['Zip']) == 10 and key['Zip'] == key2['Zip']:
                score += 80
            elif key['Zip'] and key2['Zip'] and len(key['Zip']) == 5 and len(key2['Zip']) == 5 and key['Zip'] == key2['Zip']:
                score += 5
            elif len(key['Zip']) == len(key2['Zip']) and key['Zip'] != key2['Zip']:
                score += 0
            elif (len(key['Zip']) != len(key2['Zip'])) and (key['Zip'][:5] == key2['Zip'][:5]):
                score += 5
            elif (len(key['Zip']) != len(key2['Zip'])) and (key['Zip'][:5] != key2['Zip'][:5]):
                score += 0

            if score > 100:
                score = 100
            elif score < 0:
                score = 0
            print("%10s  %10s  %10d "%(key['Counter'], key2['Counter'], score))
