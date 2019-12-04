import json
from pathlib import Path, PureWindowsPath
from difflib import get_close_matches
import operator

def getJSON():
    filename = PureWindowsPath("app\\dataFiles\\indiaAirportsList.json")
    correct_path = Path(filename) # Convert path to the right format for the current operating system

    airports = open(correct_path)
    airports = json.load(airports)
    return(airports)

def searchAirports(s):

    airports = getJSON()["airports"]

    if len(s)<5:
        for i in airports:
            if i["stnCode"]==s.upper():
                return(True, i)
    for i in airports:
        if i["stnCity"].upper()==s.upper():
            return(True, i)
    for i in airports:
        if i["stnName"].upper()==s.upper():
            return(True, i)

    for i in airports:
        if (i["stnCity"].upper()).startswith(s.upper()):
            return(True, i)
    for i in airports:
        if (i["stnName"].upper()).startswith(s.upper()):
            return(True, i)


    for i in airports:
        if operator.contains(i["stnCity"].upper(), s.upper()):
            return(True, i)
    for i in airports:
        if operator.contains(i["stnName"].upper(), s.upper()):
            return(True, i)

    stns = []
    for i in airports:
        stns.append(i["stnCity"])
    t = get_close_matches(s, stns, 1)

    if len(t)!=0:
        for i in airports:
            if i["stnCity"]==t[0]:
                return(False, i)



    stns = []
    for i in airports:
        stns.append(i["stnName"])
    t = get_close_matches(s, stns, 1)

    if len(t)!=0:
        for i in airports:
            if i["stnName"]==t[0]:
                return(False, i)

    return(False, False)

# print(searchAirports())

def makeHTML():
    airports = getJSON()["airports"]
    for i in airports:
        print("<option> " + str(i["IATA_code"]) + " - " + str(i["city_name"]) + " </option>")
        # print("<option> " + str(i[1]) + " - " + str(i[2]) + " </option>")
makeHTML()
