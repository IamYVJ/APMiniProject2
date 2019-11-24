from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
import time

global driver
driver = wd.Chrome('chromedriver')

def get_source(departure,destination,dd,mm,yyyy):
    url = 'https://flight.yatra.com/air-search-ui/dom2/trigger?type=O&viewName=normal&flexi=0&noOfSegments=1&origin=' + str(departure)+ '&originCountry=IN&destination=' + str(destination) + '&destinationCountry=IN&flight_depart_date='+str(dd)+'%2F'+str(mm)+'%2F'+str(yyyy)+'&ADT=1&CHD=0&INF=0&class=Economy&source=fresco-home&version=1.8'
    driver.get(url)
    source_code = driver.page_source
    time.sleep(1)
    driver.close()
    return(source_code)
def main():
    source = get_source('BOM','DEL',28,11,2019)

if __name__ == "__main__":
    main()