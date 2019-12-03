import json
from pathlib import Path, PureWindowsPath
from difflib import get_close_matches
import operator

def getJSON():
    filename = PureWindowsPath("app\\dataFiles\\railwayStationsList.json")
    correct_path = Path(filename) # Convert path to the right format for the current operating system

    stations = open(correct_path)
    stations = json.load(stations)
    return(stations)

def searchStations(s):

    stations = getJSON()["stations"]

    if len(s)<5:
        for i in stations:
            if i["stnCode"]==s.upper():
                return(True, i)
    for i in stations:
        if i["stnCity"].upper()==s.upper():
            return(True, i)
    for i in stations:
        if i["stnName"].upper()==s.upper():
            return(True, i)

    for i in stations:
        if (i["stnCity"].upper()).startswith(s.upper()):
            return(True, i)
    for i in stations:
        if (i["stnName"].upper()).startswith(s.upper()):
            return(True, i)


    for i in stations:
        if operator.contains(i["stnCity"].upper(), s.upper()):
            return(True, i)
    for i in stations:
        if operator.contains(i["stnName"].upper(), s.upper()):
            return(True, i)

    stns = []
    for i in stations:
        stns.append(i["stnCity"])
    t = get_close_matches(s, stns, 1)

    if len(t)!=0:
        for i in stations:
            if i["stnCity"]==t[0]:
                return(False, i)



    stns = []
    for i in stations:
        stns.append(i["stnName"])
    t = get_close_matches(s, stns, 1)

    if len(t)!=0:
        for i in stations:
            if i["stnName"]==t[0]:
                return(False, i)

    return(False, False)

# print(searchStations())

def makeHTML():
    stations = getJSON()["stations"]
    for i in stations:
        if i["stnName"]==i["stnCity"]:
            print("<option> " + str(i["stnCode"]) + " - " + str(i["stnName"]) + " </option>")
        else:
            print("<option> " + str(i["stnCode"]) + " - " + str(i["stnName"]) + " - " + str(i["stnCity"]) + " </option>")
        # print("<option> " + str(i[1]) + " - " + str(i[2]) + " </option>")
# makeHTML()
