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
# from OSDetect import osDetect

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



def trainSearch(srcStn, srcCity, destStn, destCity, dd, mm, yyyy):

    rawData = get_source(srcStn, srcCity, destStn, destCity, dd, mm, yyyy)
    traindata = gettraindata(rawData)

    for i in traindata:
        i.append(srcStn)
        i.append(srcCity)
        i.append(destStn)
        i.append(destCity)

    return(traindata)


# TEST

def test():
    srcStn = 'R'
    srcCity = 'Raipur'
    destStn = 'HWH'
    destCity = 'Kolkata'
    dd = 30
    mm = 11
    yyyy = 2019

    traindata =  trainSearch(srcStn, srcCity, destStn, destCity, dd, mm, yyyy)

    for i in traindata:
        for j in i:
            print(j)
        print()

# test()
