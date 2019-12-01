from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as OptionsCr
import json
from app.OSDetect import osDetect

global driver
driver = ""


def get_source(departureCode, arrivalCode, dd, mm, yyyy):

    syst = osDetect()

    if syst=='W':
        options = Options()
        options.headless = True
        driver = wd.Firefox(executable_path = r'drivers\Windows\geckodriver.exe', options=options)

    elif syst=='M':
        driver = wd.Chrome()

    elif syst=='L':
        options = Options()
        options.headless = True
        driver = wd.Firefox(executable_path = r'drivers/Linux/geckodriver', options=options)

    # url = "https://flight.yatra.com/air-search-ui/int2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=DEL&originCountry=IN&destination=DCA&destinationCountry=US&flight_depart_date=15/12/2019&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-home&version=1.1"
    url = 'https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=' + str(departureCode)+ '&originCountry=IN&destination=' + str(arrivalCode) + '&destinationCountry=IN&flight_depart_date='+str(dd)+'%2F'+str(mm)+'%2F'+str(yyyy)+'&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-home&version=1.8'
    driver.get(url)
    source_code = driver.page_source
    time.sleep(0.5)
    driver.close()
    rawSource = ""
    try:
        for i in source_code:
            try:
                rawSource = rawSource + i
            except:
                pass
    except:
        pass
    return(rawSource)


def jsonData(rawSource):
    soup = BeautifulSoup(rawSource, 'html5lib')
    i = 1
    jsData = ""
    for row in soup.findAll('script', attrs = {'type':'text/javascript'}):
        if i!=10:
            i = i+1
            continue
        jsData = str(row.text)
        break

    val = jsData.find('mainData')
    val = jsData.find('mainData', val+1)
    jsData = jsData[jsData.find('{'):val-10]

    return(jsData)


def searchCode(departureCode, arrivalCode, dd, mm, yyyy):
    sCode = str(departureCode) + str(arrivalCode) + str(yyyy) + str(mm) + str(dd)
    return(sCode)


def flightDetails(jsData, sCode):
    flights = []
    jsonData = json.loads(jsData)

    for i in jsonData["resultData"]:
        for j in i["fltSchedule"][sCode]:
            flight = {
            'flightID' : '',
            'xmlKey' : '',
            'baggageAllowance' : '',
            'classtype':'',
            'totalStops' : '0',
            'totalDuration' : '',
            'totalLayover' : '0',
            'airline' : '',
            'airlineCode' : '',
            'vehicleCode' : '',
            'flightNo' : '',
            'departureCityCode' : '',
            'arrivalCityCode' : '',
            'departureDate' : '',
            'arrivalDate' : '',
            'departureTime' : '',
            'arrivalTime' : '',
            'aircraft' : '',
            'departureTerminal' : '',
            'arrivalTerminal' : '',
            'mealCost' : '',
            "baseFare":"",
            "totalFare":"",
            "px":"ADT",
            "qt":"1",
            "fuelSurcharge":"0",
            "PSF":"0",
            "userDevelopmentFee":"0",
            "goodsAndServiceTax":"0",
            "GAST":"0",
            "swachhBharatCess":"0",
            "krishiKalyanCess":"0",
            "cuteFee":"0",
            "airportArrivalTax":"0",
            "developmentFee":"0",
            "otherFlightsInfo" : []
            }
            flight['flightID'] = j['ID']
            try:
                flight['xmlKey'] = j['xmlKey']
            except:
                pass
            for k in j["OD"]:
                flight['baggageAllowance'] = k['bga']
                try:
                    flight['classtype'] = k['classtype']
                except:
                    pass
                flight['totalDuration'] = k['tdu']
                try:
                    flight['totalLayover'] = k['tlot']
                except:
                    pass
                try:
                    flight['totalStops'] = k['ts']
                except:
                    pass
                if len(k["FS"])==1:
                    flight['airlineCode'] = k['FS'][0]['ac']
                    flight['airline'] = i["fltSchedule"]["airlineNames"][flight['airlineCode']]
                    flight['vehicleCode'] = k['FS'][0]['vac']
                    flight['flightNo'] = k['FS'][0]['fl']
                    flight['departureCityCode'] = k['FS'][0]['dac']
                    flight['arrivalCityCode'] = k['FS'][0]['aac']
                    flight['departureDate'] = k['FS'][0]['ddt']
                    flight['arrivalDate'] = k['FS'][0]['adt']
                    flight['departureTime'] = k['FS'][0]['dd']
                    flight['arrivalTime'] = k['FS'][0]['ad']
                    flight['aircraft'] = k['FS'][0]['eq']
                    # flight['baggageAllowance'] = k['FS'][0]['bga']
                    try:
                        flight['departureTerminal'] = k['FS'][0]['dt']
                    except:
                        pass
                    try:
                        flight['arrivalTerminal'] = k['FS'][0]['at']
                    except:
                        pass
                    # flight['classtype'] = k['FS'][0]['classtype']
                    flight['mealCost'] = k['FS'][0]['ml']
                else:
                    otherFlights = []
                    for l in k['FS']:
                        otherFlight = {
                        # 'flightID' : '',
                        # 'xmlKey' : '',
                        'baggageAllowance' : '',
                        'classtype':'',
                        # 'totalStops' : '',
                        # 'totalDuration' : '',
                        # 'totalLayover' : '',
                        'airline' : '',
                        'airlineCode' : '',
                        'vehicleCode' : '',
                        'flightNo' : '',
                        'departureCityCode' : '',
                        'arrivalCityCode' : '',
                        'departureDate' : '',
                        'arrivalDate' : '',
                        'departureTime' : '',
                        'arrivalTime' : '',
                        'aircraft' : '',
                        'departureTerminal' : '',
                        'arrivalTerminal' : '',
                        'mealCost' : ''
                        }
                        # "baseFare":"",
                        # "totalFare":"",
                        # "px":"",
                        # "qt":"",
                        # "fuelSurcharge":"",
                        # "PSF":"",
                        # "userDevelopmentFee":"",
                        # "goodsAndServiceTax":"",
                        # "GAST":"",
                        # "swachhBharatCess":"",
                        # "krishiKalyanCess":"",
                        # "cuteFee":"",
                        # "airportArrivalTax":"",
                        # "developmentFee":""
                        # }
                        otherFlight['airlineCode'] = l['ac']
                        otherFlight['airline'] = i["fltSchedule"]["airlineNames"][otherFlight['airlineCode']]
                        otherFlight['vehicleCode'] = l['vac']
                        otherFlight['flightNo'] = l['fl']
                        otherFlight['departureCityCode'] = l['dac']
                        otherFlight['arrivalCityCode'] = l['aac']
                        otherFlight['departureDate'] = l['ddt']
                        otherFlight['arrivalDate'] = l['adt']
                        otherFlight['departureTime'] = l['dd']
                        otherFlight['arrivalTime'] = l['ad']
                        otherFlight['aircraft'] = l['eq']
                        otherFlight['baggageAllowance'] = l['bga']
                        try:
                            otherFlight['departureTerminal'] = l['dt']
                        except:
                            pass
                        try:
                            otherFlight['arrivalTerminal'] = l['at']
                        except:
                            pass
                        try:
                            otherFlight['classtype'] = l['classtype']
                        except:
                            pass
                        otherFlight['mealCost'] = l['ml']
                        otherFlights.append(otherFlight)
                    flight['otherFlightsInfo'] = otherFlights
            flights.append(flight)


    for i in jsonData["resultData"]:
        for j in i["fareDetails"][sCode]:
            fCode = str(j)
            for k in flights:
                if k["flightID"]==fCode:
                    try:
                        k['baseFare'] = i["fareDetails"][sCode][j]["O"]["ADT"]["bf"]
                    except:
                        pass
                    try:
                        k['totalFare'] = i["fareDetails"][sCode][j]["O"]["ADT"]["tf"]
                    except:
                        pass
                    try:
                        k['px'] = i["fareDetails"][sCode][j]["O"]["ADT"]["px"]
                    except:
                        pass
                    try:
                        k['qt'] = i["fareDetails"][sCode][j]["O"]["ADT"]["qt"]
                    except:
                        pass
                    try:
                        k['fuelSurcharge'] = i["fareDetails"][sCode][j]["O"]["ADT"]["YQ"]
                    except:
                        pass
                    try:
                        k['PSF'] = i["fareDetails"][sCode][j]["O"]["ADT"]["PSF"]
                    except:
                        pass
                    try:
                        k['userDevelopmentFee'] = i["fareDetails"][sCode][j]["O"]["ADT"]["UDF"]
                    except:
                        pass
                    try:
                        k['goodsAndServiceTax'] = i["fareDetails"][sCode][j]["O"]["ADT"]["GST"]
                    except:
                        pass
                    try:
                        k['GAST'] = i["fareDetails"][sCode][j]["O"]["ADT"]["GAST"]
                    except:
                        pass
                    try:
                        k['swachhBharatCess'] = i["fareDetails"][sCode][j]["O"]["ADT"]["SBC"]
                    except:
                        pass
                    try:
                        k['krishiKalyanCess'] = i["fareDetails"][sCode][j]["O"]["ADT"]["KKC"]
                    except:
                        pass
                    try:
                        k['cuteFee'] = i["fareDetails"][sCode][j]["O"]["ADT"]["TF"]
                    except:
                        pass
                    try:
                        k['airportArrivalTax'] = i["fareDetails"][sCode][j]["O"]["ADT"]["WC"]
                    except:
                        pass
                    try:
                        k['developmentFee'] = i["fareDetails"][sCode][j]["O"]["ADT"]["DF"]
                    except:
                        pass
                    break

    return(flights)

def flightSearch(departureCode, arrivalCode, dd, mm, yyyy):

    for i in range(3):
        flights = []
        try:
            sCode = searchCode(departureCode, arrivalCode, dd, mm, yyyy)
            rawSource = get_source(departureCode, arrivalCode, dd, mm, yyyy)
            # print(rawSource)
            jsData = jsonData(rawSource)
            # print(jsData)
            flights = flightDetails(jsData, sCode)
            break
        except Exception as e:
            print("#" + str(i+1) + ": Error Found")
            print(e)
            print()
            continue

    return(flights)



def testCase():
    departureCode = "DEL"
    arrivalCode = "BLR"
    dd = "15"
    mm = "12"
    yyyy = "2019"
    flights = flightSearch(departureCode, arrivalCode, dd, mm, yyyy)

    for i in flights:
        print(i)

# from OSDetect import osDetect
# testCase()




# ERROR CHECK CODE ------>
#
# for i in range(3):
#     try:
#         sCode = searchCode(departureCode, arrivalCode, dd, mm, yyyy)
#         break
#     except Exception as e:
#         print("#" + str(i+1) + ": Error Found in searchCode")
#         print(e)
#         print()
#         continue
#
# for i in range(3):
#     flights = []
#     try:
#         rawSource = get_source(departureCode, arrivalCode, dd, mm, yyyy)
#         break
#     except Exception as e:
#         print("#" + str(i+1) + ": Error Found in get_source")
#         print(e)
#         print()
#         continue
#
# for i in range(3):
#     try:
#         jsData = jsonData(rawSource)
#         break
#     except Exception as e:
#         print("#" + str(i+1) + ": Error Found in jsonData")
#         print(e)
#         print()
#         continue
#
# for i in range(3):
#     try:
#         flights = flightDetails(jsData, sCode)
#         break
#     except Exception as e:
#         print("#" + str(i+1) + ": Error Found in flightDetails")
#         print(e.message)
#         print()
#         continue
