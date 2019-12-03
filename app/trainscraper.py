from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as OptionsCr
from app.OSDetect import osDetect
from app.railwayStations import searchStations

global driver
driver = ""

def get_source(srcStn, srcCity, destStn, destCity, dd, mm, yyyy):

    syst = osDetect()


    if syst=='W':
        options = Options()
        options.headless = True
        # path = os.path.dirname(os.path.realpath(__file__))
        # +"\\drivers\\Windows\\geckodriver"
        driver = wd.Firefox(executable_path = r'drivers\Windows\geckodriver.exe', options=options)
    elif syst=='M':

        # options = Options()
        # options.headless = True
        # driver = wd.Firefox(executable_path = r'drivers/MacOS/geckodriver', options=options)
        # driver = wd.Firefox(executable_path = r'//usr/local/bin/geckodriver', options=options)

        # options = wd.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument("--test-type")
        # options.binary_location = "/usr/bin/chromium"
        # driver = wd.Chrome(chrome_options=options)

        # chrome_options = wd.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # driver = wd.Chrome(options = chrome_options)


        # options = wd.ChromeOptions()
        # options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        # options.add_argument('headless')
        # driver = wd.Chrome(chrome_options=options)

        driver = wd.Chrome()

        # chrome_options = OptionsCr()
        # chrome_options.add_argument("--headless")
        # driver = wd.Chrome('chromedriver')
        # driver = wd.Chrome(executable_path='//Users/raj.burad7/Desktop/APMiniProject2/app/chromedriver',options=chrome_options)
        # driver = wd.Chrome(options=chrome_options)
        # driver = wd.Chrome(executable_path='drivers/MacOS/geckodriver',options=chrome_options)
        # driver = wd.Chrome(executable_path='drivers/MacOS/geckodriver')

        # Other Code

        # # chrome_options = wd.ChromeOptions()
        # chrome_options = OptionsCr()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox') # required when running as root user. otherwise you would get no sandbox errors.
        # driver = wd.Chrome(executable_path='drivers/MacOS/geckodriver', chrome_options=chrome_options)

    elif syst=='L':
        #Linux Code
        options = Options()
        options.headless = True
        driver = wd.Firefox(executable_path = r'drivers/Linux/geckodriver', options=options)


    srcStn = srcStn.strip()
    srcCity = srcCity.strip()
    srcCity = srcCity.replace(' ', '&')
    destStn = destStn.strip()
    destCity = destCity.strip()
    destCity = destCity.replace(' ', '&')

    url = 'https://railways.makemytrip.com/listing?date=' + str(yyyy) + str(mm) + str(dd) + '&srcStn=' + srcStn + '&srcCity=' + srcCity + '&destStn=' + destStn + '&destCity=' + destCity + '&classCode='

    # options = Options()
    # options.headless = True
    # driver = wd.Firefox(options=options)

    # chrome_options = Options() #THIS WAS WORKING
    # # chrome_options.add_argument("--headless")
    # driver = wd.Chrome(executable_path='//Users/raj.burad7/Desktop/APMiniProject2/app/chromedriver',options=chrome_options)

    driver.get(url)
    source_code = driver.page_source
    time.sleep(5)
    driver.close()
    # print(source_code)
    modSource = ""
    try:
        for i in source_code:
            modSource = modSource + i
    except:
        bool = 0

    raw = ""

    for i in modSource:
        try:
            if(i!='\u20b9' and i!='\ufffd'):
                raw = raw + i
        except:
            continue

    return(raw)

def gettraindata(rawData):

    soup = BeautifulSoup(rawData, 'html5lib')

    # print(soup.prettify())

    traindata = []

    for row1 in soup.findAll('div', attrs = {'class':'railInfo railTitle'}):

        train = []

        temp = row1.text

        hl = temp.find('#')
        tr = temp[1:hl-2]
        # print(tr)

        temp = temp[hl:]
        hl = temp.find('D')
        trainno = temp[:hl-1]
        # print(trainno)

        departs = ""

        for row in row1.findAll('span', attrs = {'class':'greenText latoBold'}):
            departs = departs + " " + (row.text)
        departs = departs.strip()
        # print(departs)

        train.append(tr)
        train.append(trainno)
        train.append(departs)

        traindata.append(train)

    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railInfo railDeparture'}):
        tt = row1.text
        tp = tt.find('M')

        at = tt[1:tp+1] + " " + tt[tp+4:tp+8]
        att = tt[tp+8:]
        traindata[i].append(at)
        traindata[i].append(att)
        i = i+1


    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railInfo textCenter railDuration'}):
        tt = row1.text
        dr = tt[:tt.find('V')-1]

        traindata[i].append(dr)
        i = i+1


    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railInfo railArrival'}):
        tt = row1.text
        tp = tt.find('M')

        dt = tt[1:tp+1] + " " + tt[tp+4:tp+8]
        dtt = tt[tp+8:]
        traindata[i].append(dt)
        traindata[i].append(dtt)
        i = i+1

    i = 0
    for row1 in soup.findAll('div', attrs = {'class':'railClassBox'}):
        allclasses = []
        classes = []
        tt = row1.text
        ti = 0
        tp = tt.find('ago')
        while(tp!=-1):
            allclasses.append(tt[ti:tp+3])
            ti = tp+3
            tp = tt.find('ago', ti)

        for j in allclasses:
            ttt = []
            tp = 0
            if j.find('Click to update')!=-1:
                j = j[j.find('Click to update')+14:]
            if j.find('AC Chair Car')!=-1:
                ttt.append('AC Chair Car')
                tp = len('AC Chair Car')
            elif j.find('Executive Chair Car')!=-1:
                ttt.append('Executive Chair Car')
                tp = len('Executive Chair Car')
            elif j.find('3 Tier AC')!=-1:
                ttt.append('3 Tier AC')
                tp = len('3 Tier AC')
            elif j.find('2 Tier AC')!=-1:
                ttt.append('2 Tier AC')
                tp = len('2 Tier AC')
            elif j.find('1st Class AC')!=-1:
                ttt.append('1st Class AC')
                tp = len('1st Class AC')
            elif j.find('Executive Anubhuti')!=-1:
                ttt.append('Executive Anubhuti')
                tp = len('Executive Anubhuti')
            elif j.find('Sleeper')!=-1:
                ttt.append('Sleeper')
                tp = len('Sleeper')
            elif j.find('Second Sitting')!=-1:
                ttt.append('Second Sitting')
                tp = len('Second Sitting')
            # elif j.find('')!=-1:
            #     ttt.append('')
            #     tp = len('')
            # elif j.find('')!=-1:
            #     ttt.append('')
            #     tp = len('')
            else:
                print("UNKNOWN CLASS FOUND: ")
                print(j)
                print()
                continue

            fare = ""

            for k in j[tp:]:
                if k.isdigit():
                    fare = fare + k
                    tp = tp + 1
                else:
                    break
            ttt.append(fare)

            up = j[tp:].find('Updated')

            ttt.append(j[tp:tp+up])
            ttt.append(j[tp+up:])

            classes.append(ttt)
            # print(ttt)
            # print(j[tp:])
        # print(classes)
        # print()
        traindata[i].append(classes)
        i = i+1
    return(traindata)


def fixTrainData(traindata):
    trainDataDict = []
    for i in traindata:

        train = {
            "trainName" : "",
             "trainNo" : "",
             "days" : "",
             "departureTime" : "",
             "depStnInfo" : "",
             "duration" : "",
             "arrivalTime" : "",
             "arrStnInfo" : "",
             "classes" : "",
             "departureCity" : "",
             "departureStnCode" : "",
             "departureStn" : "",
             "arrivalCity" : "",
             "arrivalStnCode" : "",
             "arrivalStn" : "",
             "departureDate" : "",
             "arrivalDate" : ""
            }

        train["trainName"] = i[0]
        train["trainNo"] = i[1]
        train["days"] = i[2]
        train["departureTime"] = i[3]
        train["depStnInfo"] = i[4]
        train["duration"] = i[5]
        train["arrivalTime"] = i[6]
        train["arrStnInfo"] = i[7]
        # train["classes"] = i[8]
        classes = []
        for j in i[8]:
            tclass = {
            "className" : "",
            "price" : "",
            "availability" : "",
            "update" : ""
            }
            tclass["className"] = j[0]
            tclass["price"] = j[1]
            tclass["availability"] = j[2]
            tclass["update"] = j[3]
            classes.append(tclass)
        train["classes"] = classes
        train["departureCity"] = i[10]
        train["departureStnCode"] = i[9]
        train["departureStn"] = i[14]
        train["arrivalCity"] = i[12]
        train["arrivalStnCode"] = i[11]
        train["arrivalStn"] = i[15]
        train["departureDate"] = i[13]
        # train["arrivalDate"] =
        trainDataDict.append(train)
    return(trainDataDict)

def trainSearch(searchDep,  searchArr, dd, mm, yyyy):
    # return([{'trainName': 'GITANJALI EX', 'trainNo': '#12859', 'days': 'S   M   T   W   T   F   S', 'departureTime': '11:35 PM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '12h 55m', 'arrivalTime': '12:30 PM  Fri', 'arrStnInfo': 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', 'classes': [{'className': 'Sleeper', 'price': '440', 'availability': 'RLWL 39', 'update': 'Updated 1 day ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}, {'trainName': 'PBR HOWRAH EX', 'trainNo': '#12905', 'days': 'M   T   F', 'departureTime': '2:30 PM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '13h 5m', 'arrivalTime': '3:35 AM  Fri', 'arrStnInfo': 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', 'classes': [{'className': 'Sleeper', 'price': '440', 'availability': 'RLWL 18', 'update': 'Updated 18 hrs ago'}, {'className': '3 Tier AC', 'price': '1165', 'availability': 'RLWL 12', 'update': 'Updated 18 hrs ago'}, {'className': '2 Tier AC', 'price': '1660', 'availability': 'RLWL 6', 'update': 'Updated 18 hrs ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}, {'trainName': 'AZAD HIND EX', 'trainNo': '#12129', 'days': 'S   M   T   W   T   F   S', 'departureTime': '2:52 PM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '13h 23m', 'arrivalTime': '4:15 AM  Fri', 'arrStnInfo': 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', 'classes': [{'className': 'Sleeper', 'price': '440', 'availability': 'RLWL 16', 'update': 'Updated 1 day ago'}, {'className': '3 Tier AC', 'price': '1165', 'availability': 'RLWL 10', 'update': 'Updated 1 day ago'}, {'className': '2 Tier AC', 'price': '1660', 'availability': 'RLWL 4', 'update': 'Updated 1 day ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}, {'trainName': 'HOWRAH MAI', 'trainNo': '#12809', 'days': 'S   M   T   W   T   F   S', 'departureTime': '4:10 PM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '13h 40m', 'arrivalTime': '5:50 AM  Fri', 'arrStnInfo': 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', 'classes': [{'className': 'Sleeper', 'price': '440', 'availability': 'RLWL 31', 'update': 'Updated 1 day ago'}, {'className': '3 Tier AC', 'price': '1165', 'availability': 'RLWL 18', 'update': 'Updated 15 hrs ago'}, {'className': '2 Tier AC', 'price': '1660', 'availability': 'RLWL 11', 'update': 'Updated 15 hrs ago'}, {'className': '1st Class AC', 'price': '2815', 'availability': 'RLWL 1', 'update': 'Updated 1 day ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}, {'trainName': 'HOWRAH EXPRES', 'trainNo': '#12833', 'days': 'S   M   T   W   T   F   S', 'departureTime': '11:05 PM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '14h 25m', 'arrivalTime': '1:30 PM  Fri', 'arrStnInfo': 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', 'classes': [{'className': 'Sleeper', 'price': '445', 'availability': 'RLWL 35', 'update': 'Updated 2 days ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}, {'trainName': 'KARMABHOOMI EX', 'trainNo': '#22511', 'days': 'T', 'departureTime': '6:05 AM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '15h 25m', 'arrivalTime': '9:30 PM  Thu', 'arrStnInfo': 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', 'classes': [{'className': 'Sleeper', 'price': '440', 'availability': 'RLWL 77', 'update': 'Updated 18 hrs ago'}, {'className': '3 Tier AC', 'price': '1165', 'availability': 'RLWL 30', 'update': 'Updated 1 day ago'}, {'className': '2 Tier AC', 'price': '1660', 'availability': 'Booking not allowed', 'update': 'Updated 1 day ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}, {'trainName': 'LTT SHALIMAR E', 'trainNo': '#18029', 'days': 'S   M   T   W   T   F   S', 'departureTime': '7:42 PM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '16h 38m', 'arrivalTime': '12:20 PM  Fri', 'arrStnInfo': 'SHMDifferentYou searched for trains arriving in HWH (Kolkata), but this train arrives in SHM (Shalimar).HWH R SHMShalimar', 'classes': [{'className': '3 Tier AC', 'price': '', 'availability': 'C1120RLWL 11', 'update': 'Updated 1 day ago'}, {'className': '2 Tier AC', 'price': '1615', 'availability': 'RLWL 3', 'update': 'Updated 1 day ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}, {'trainName': 'SAMARSATA EX', 'trainNo': '#12151', 'days': 'T   F', 'departureTime': '3:40 PM  Thu', 'depStnInfo': 'RYou searched for trains departing from R(Raipur), but this train departs from R (Raipur Jn)R R HWHRaipur Jn', 'duration': '16h 45m', 'arrivalTime': '8:25 AM  Fri', 'arrStnInfo': 'HWHYou searched for trains arriving in HWH (Kolkata), but this train arrives in HWH (Howrah Jn).HWH R HWHHowrah Jn', 'classes': [{'className': 'Sleeper', 'price': '480', 'availability': 'RLWL 23', 'update': 'Updated 13 hrs ago'}, {'className': '3 Tier AC', 'price': '1270', 'availability': 'RLWL 14', 'update': 'Updated 1 day ago'}, {'className': '2 Tier AC', 'price': '1820', 'availability': 'RLWL 4', 'update': 'Updated 13 hrs ago'}, {'className': '1st Class AC', 'price': '3100', 'availability': 'RLWL 1', 'update': 'Updated 3 days ago'}], 'departureCity': '', 'departureStnCode': '', 'arrivalCity': '', 'arrivalStnCode': '', 'departureDate': '', 'arrivalDate': ''}])

    if '-' in searchDep:
        searchDep = searchDep[:searchDep.find('-')].strip()

    boold, dep = searchStations(searchDep)

    if boold==False:
        return([0])

    print(dep)

    if '-' in searchArr:
        searchArr = searchArr[:searchArr.find('-')].strip()

    boola, arr = searchStations(searchArr)

    if boola==False:
        return([1])

    print(arr)

    srcStn = dep["stnCode"]
    srcCity = dep["stnCity"]
    destStn = arr["stnCode"]
    destCity = arr["stnCity"]
    rawData = get_source(srcStn, srcCity, destStn, destCity, dd, mm, yyyy)
    traindata = gettraindata(rawData)

    for i in traindata:
        i.append(srcStn)
        i.append(srcCity)
        i.append(destStn)
        i.append(destCity)
        i.append(str(dd)+'-'+str(mm)+'-'+str(yyyy))
        i.append(dep["stnName"])
        i.append(arr["stnName"])
    traindata = fixTrainData(traindata)

    return(traindata)


# TEST

def test():
    srcStn = 'R'
    srcCity = 'Raipur'
    destStn = 'HWH'
    destCity = 'Kolkata'
    dd = 12
    mm = 12
    yyyy = 2019

    traindata =  trainSearch(srcStn, srcCity, destStn, destCity, dd, mm, yyyy)

    # print(traindata)

    for i in traindata:
        print(i)
        print()

# from OSDetect import osDetect
# test()
