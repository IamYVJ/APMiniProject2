from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

global driver
driver = ""

def get_source():

    options = Options()
    # options.headless = True
    driver = wd.Firefox(options=options)

    url = 'https://railways.makemytrip.com/listing?date=20191127&srcStn=NDLS&srcCity=New%20Delhi&destStn=CNB&destCity=Kanpur&classCode='
    driver.get(url)
    source_code = driver.page_source
    time.sleep(0.5)
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
            raw = raw + i
        except:
            continue

    return(raw)

aa = get_source()




soup = BeautifulSoup(aa, 'html5lib')

for row1 in soup.findAll('div', attrs = {'class':'railInfo railTitle'}):
    print(row1.text)
    print()



for row1 in soup.findAll('div', attrs = {'class':'railInfo railDeparture'}):
    print(row1.text)
    print()



for row1 in soup.findAll('div', attrs = {'class':'railInfo textCenter railDuration'}):
    print(row1.text)
    print()



for row1 in soup.findAll('div', attrs = {'class':'railInfo railArrival'}):
    print(row1.text)
    print()



for row1 in soup.findAll('div', attrs = {'class':'railClassBox'}):
    print(row1.text)
    print()
