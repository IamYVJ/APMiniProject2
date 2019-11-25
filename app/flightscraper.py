from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from bs4 import BeautifulSoup


global driver
driver = ""


def flightData(rawData):
    soup = BeautifulSoup(rawData, 'html5lib')

    flights = [] # Departure City, Arrival City, Airline, Flight No, Departure Time, Arrival Time, Flight Duration,, No of stops

    for row1 in soup.findAll('div', attrs = {'class':'schedule v-aligm-t pr'}):

        flight = []

        t1 = row1.findAll('div', attrs = {'class':'i-b pr'})
        for row in t1:
            dt = str(row)
            dt = dt[20:25]

            ar = str(row.p)
            ar = ar[71:]
            ar = ar[:ar.find('<')]

            fn = row.span.text


        t2 = row1.findAll('p', attrs = {'class':'fs-10 font-lightgrey no-wrap city ellipsis'})
        for row in t2:
            flight.append(row.text)

        t3 = row1.findAll('p', attrs = {'autom':'arrivalTimeLabel'})
        for row in t3:
            at = row.text

        t4 = row1.findAll('p', attrs = {'autom':'durationLabel'})
        for row in t4:
            dr = row.text

        t5 = row1.findAll('span', attrs = {'class':'cursor-default'})
        for row in t5:
            st = row.text

        flight.append(ar)
        flight.append(fn)
        flight.append(dt)
        flight.append(at)
        flight.append(dr)
        flight.append(st)

        flights.append(flight)

    # print(flights)

    return(flights)


def get_source(departureCode, arrivalCode, dd, mm, yyyy):

    driver = wd.Firefox()

    url = 'https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=' + str(departureCode)+ '&originCountry=IN&destination=' + str(arrivalCode) + '&destinationCountry=IN&flight_depart_date='+str(dd)+'%2F'+str(mm)+'%2F'+str(yyyy)+'&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-home&version=1.8'
    driver.get(url)
    source_code = driver.page_source
    time.sleep(1)
    driver.close()
    modSource = ""
    try:
        for i in source_code:
            modSource = modSource + i
    except:
        bool = 0
    return(modSource)


def flightSearch(departureCode, arrivalCode, dd, mm, yyyy):

    source = get_source(departureCode, arrivalCode, dd, mm, yyyy)
    flights = flightData(source)

    return(flights)

def testCase():
    departureCode = "DEL"
    arrivalCode = "BOM"
    dd = 26
    mm = 11
    yyyy = 2019
    flights = flightSearch(departureCode, arrivalCode, dd, mm, yyyy)
    print(flights)

testCase()
