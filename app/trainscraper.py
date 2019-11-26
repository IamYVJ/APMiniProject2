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
            # print(i, end="")
            if(i!='\u20b9' and i!='\ufffd'):
                raw = raw + i
        except:
            continue

    return(raw)

aa = get_source()

# print()
# print()
# print()
# print()


soup = BeautifulSoup(aa, 'html5lib')

# print(soup.prettify())

for row1 in soup.findAll('div', attrs = {'class':'railInfo railTitle'}):

    # train = []
    #
    # for row in row1.findAll('p', attrs = {'class':'appendBottom10 latoBlack font22 blackText'}):
    #     train.append(row.text[1:])


    temp = row1.text

    hl = temp.find('#')
    train = temp[1:hl-2]
    print(train)

    temp = temp[hl:]
    hl = temp.find('D')
    trainno = temp[:hl-1]
    print(trainno)

    departs = []

    for row in row1.findAll('span', attrs = {'class':'greenText latoBold'}):
        departs.append(row.text)

    print(departs)

print()

for row1 in soup.findAll('span', attrs = {'class':'font22 latoBold'}):
    print(row1.text)
    # print()

print()

for row1 in soup.findAll('div', attrs = {'class':'railInfo railDeparture'}):
    tt = row1.text
    print(tt[:tt.find('M')+1], end=" ")
    print(row1.text[tt.find('M')+4:tt.find('M')+8])
    print(row1.text[tt.find('M')+8:])
    # print()

print()

for row1 in soup.findAll('div', attrs = {'class':'railInfo textCenter railDuration'}):
    tt = row1.text
    print(tt[:tt.find('V')-1])
    # print()

print()

for row1 in soup.findAll('div', attrs = {'class':'railInfo railArrival'}):
    tt = row1.text
    print(tt[:tt.find('M')+1], end=" ")
    print(row1.text[tt.find('M')+4:tt.find('M')+8])
    print(row1.text[tt.find('M')+8:])
    # print()

print()

for row1 in soup.findAll('div', attrs = {'class':'railClassBox'}):
    classes = []
    tt = row1.text
    ti = 0
    tp = tt.find('ago')
    while(tp!=-1):
        tclass = []
        tclass.append(tt[ti:tp+3])
        ti = tp+3
        tp = tt.find('ago', ti)
        classes.append(tclass)
    print(classes)
    # print()
