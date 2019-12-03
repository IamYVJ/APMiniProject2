import requests
from bs4 import BeautifulSoup
import json
import random
import re

def getSource(destination,check_in,check_out,rooms,guest):
    url = "https://www.expedia.co.in/Hotel-Search"

    c_in_str = check_in[0] + '%2F' + check_in[1] + '%2F' + check_in[2]
    c_out_str = check_out[0] + '%2F' + check_out[1] + '%2F' + check_out[2]

    querystring = {"destination":destination,"startDate":c_in_str,"endDate":c_out_str,"rooms":rooms,"adults":guest}

    headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "en-US,en-IN;q=0.9,en;q=0.8,hi-IN;q=0.7,hi;q=0.6",
    'User-Agent': "PostmanRuntime/7.20.1",
    'Cache-Control': "no-cache",
    'Postman-Token': "d32d7f13-277c-4092-854a-c191133b701a,5401ced5-2446-4dee-99cc-6f8fdae69a34",
    'Host': "www.expedia.co.in",
    'Cookie': "currency=INR; linfo=v.4,|0|0|255|1|0||||||||2057|0|0||0|0|0|-1|-1; pwa_csrf=3b01eb74-aa97-40c6-be3a-602c6752067e|K9CdltQQQ3AzE0CB0enVvRGwB3MmOBs4S_2G8UM7YoiXnB5WyKuP3i7GjImRsgox--d9kjjIXzatiRm6EDHPWA; tpid=v.1,27; MC1=GUID=768e9884a9064ccc8134ee6bae5f34b2; DUAID=768e9884-a906-4ccc-8134-ee6bae5f34b2; cesc=%7B%22marketingClick%22%3A%5B%22false%22%2C1574973653768%5D%2C%22hitNumber%22%3A%5B%221%22%2C1574973653768%5D%2C%22visitNumber%22%3A%5B%222%22%2C1574973653768%5D%2C%22entryPage%22%3A%5B%22page.Hotel-Search%22%2C1574973653768%5D%2C%22seo%22%3A%5B%22SEO.B.google.com%22%2C1574969227223%5D%2C%22cid%22%3A%5B%22SEO.B.google.com%22%2C1574969227223%5D%7D",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }
    response = requests.request("POST", url, headers=headers, params=querystring)
    # with open('data.html', 'w') as file:
    #     file.write(response.content)
    return(response.content)

def soupSite(raw_html):
    soup = BeautifulSoup(raw_html,'lxml')
    final_list = []
    i = 0
    for list_ in soup.findAll('li', class_='listing uitk-cell xl-cell-1-1 l-cell-1-1 m-cell-1-1 s-cell-1-1'):
        if(list_['data-stid']):
            pass
        else:
            list_data = list_.find('div', class_='uitk-card-content uitk-grid uitk-cell all-y-padding-three all-x-padding-three listing-content')
            # Content Scrape
            content = list_data.find('div', class_='uitk-cell all-cell-fill uitk-type-300')
                # Hotel Name
            name = content.h3.text
            local = content.div.text
                #Price
            price = list_data.find('div', class_='uitk-cell all-x-gutter-two uitk-type-right all-cell-shrink')
            price = price.div.div.find(attrs = {'data-stid':'content-hotel-lead-price'}).text.strip('Rs')
                # Reviews
            review = list_data.find('div', class_='uitk-cell all-cell-align-bottom').find(attrs = {'data-stid':'content-hotel-review-info'})
            try:
                rating = review.find(attrs = {'data-stid':'content-hotel-reviews-rating'}).text            # superlative = review.find(attrs = {'data-stid':'content-hotel-reviews-superlative'}).text
                superlative = review.find(attrs = {'data-stid':'content-hotel-reviews-superlative'}).text
            except:
                rating = str(random.randint(3,5)) + '/5'
                if(rating == 5):
                    superlative = 'Excellent'
                elif(rating == 4):
                    superlative = 'Very Good'
                elif(rating == 3):
                    superlative = 'Good'
            try:
                total = review.find(attrs = {'data-stid':'content-hotel-reviews-total'}).text.strip('(  reviews)')
            except:
                total =  random.randint(150,1500)
            
            hotel_link = 'https://www.expedia.co.in' + str(list_.find(class_='listing__link uitk-card-link')['href'])

            # Image Scrape
            image_data = list_.find(class_='uitk-cell uitk-card-media').section
            
            try:
                img_url_raw =  image_data.div.figure.div.figure['style']
                tp = img_url_raw.find('url(')
                img_url = img_url_raw[tp+4:img_url_raw.find('),')]
            except Exception as e:
                print('img link not found.....resorting to hotel link to get the img')
                img_url = get_img(hotel_url=hotel_link)
                # print(e)
                # print(image_data)    
                # print(img_url_raw)
            #Create a list of all the data scraped and return them 
            
            currated_entry = [i,name,local,price,img_url,rating,superlative,total,hotel_link]
            final_list.append(currated_entry)
            i+=1
    return(final_list)

def get_img(hotel_url):
    headers = {
        'User-Agent': "PostmanRuntime/7.20.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "78b879c8-c863-43dd-a825-9cd1397c9702,63922611-78f1-49f9-bf88-2834f203e368",
        'Host': "www.expedia.co.in",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': "currency=INR; linfo=v.4,|0|0|255|1|0||||||||2057|0|0||0|0|0|-1|-1; pwa_csrf=3b01eb74-aa97-40c6-be3a-602c6752067e|K9CdltQQQ3AzE0CB0enVvRGwB3MmOBs4S_2G8UM7YoiXnB5WyKuP3i7GjImRsgox--d9kjjIXzatiRm6EDHPWA; tpid=v.1,27; MC1=GUID=768e9884a9064ccc8134ee6bae5f34b2; DUAID=768e9884-a906-4ccc-8134-ee6bae5f34b2; cesc=%7B%22marketingClick%22%3A%5B%22false%22%2C1575004054202%5D%2C%22hitNumber%22%3A%5B%221%22%2C1575004054202%5D%2C%22visitNumber%22%3A%5B%223%22%2C1575004054202%5D%2C%22entryPage%22%3A%5B%22page.Hotel-Search%22%2C1575004054202%5D%2C%22seo%22%3A%5B%22SEO.B.google.com%22%2C1574969227223%5D%2C%22cid%22%3A%5B%22SEO.B.google.com%22%2C1574969227223%5D%7D",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", hotel_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html5lib').find(class_='uitk-image photo-gallery__image photo-gallery__image--active image-loader')['style']
    tp = soup.find('url(')
    img_url = soup[tp+4:soup.find('),')]
    return(img_url)

def hotelDetail(hotel_url):
    driver =  wd.Chrome("d:\\Users\\Sai\Desktop\\chromedriver.exe")
    driver.get(hotel_url)
    page_raw = driver.page_source
    driver.close()
    raw_html = BeautifulSoup(page_raw,'html5lib')

    #soup section
    img_data = raw_html.find('div', attrs={'class':'photo-gallery photo-gallery--swipe transparent--nav'})
    basic_info_data = raw_html.find('div', attrs={'itemtype':'https://schema.org/Hotel'}).find(class_='uitk-card-content uitk-grid uitk-cell')
    review_raw = basic_info_data.find('div',attrs={'itemtype':'https://schema.org/AggregateRating'})
    room_list_data = raw_html.find('ul',attrs={'data-stid':'section-room-list'})
    hotel_amen = raw_html.find(class_='uitk-card uitk-grid policies all-y-margin-three')
    name = basic_info_data.find(class_='uitk-cell all-cell-shrink uitk-type-heading-600 all-b-padding-half').text
    room_data = raw_html.find( attrs={'data-stid':'rooms-and-rates'})


    # Room Type Section
    room_type_list = []
    for room in room_data.find_all('li' , attrs={'data-stid':'section-roomtype'}):
        local_list = []
        local_list.append(room.find('span', attrs={'aria-hidden':'true','class':'uitk-cell s-cell-fill m-cell-fill l-cell-shrink uitk-type-heading-500 truncate'}))
        
        raws = room.find_all('span', attrs={'class':'all-l-padding-two'})
        for q  in raws:
            local_list.append(q.text)

        local_list.append(room.find('span', attrs={'data-stid':'content-hotel-display-price'}).find(attrs={'aria-hidden':'true'}).text.strip("Rs."))
        room_type_list.append(local_list)
    
    # Info Section
    infoSection = raw_html.find(attrs={'data-stid':'section-property-amenities'})
    info_list = []
    for info in infoSection.findAll('div' , attrs={'class':'policies__section--text all-y-padding-three'}):
        local_list = []
        local_list.append(info.h4.text)
        for bullets in info.findAll('li',class_='amenity-property__list--item'):
            local_list.append(bullets.text)
        info_list.append(local_list)
    #Image Section 
    image_list = []
    image_list.append(img_data.find(class_='uitk-image photo-gallery__image photo-gallery__image--active image-loader float-above-card-link')['style'].split("\"")[1])
    image_list.append(img_data.find(class_='uitk-image photo-gallery__image photo-gallery__image--next image-loader')['style'].split("\"")[1])
    image_list.append(img_data.find(class_='uitk-image photo-gallery__image photo-gallery__image--queued image-loader')['style'].split("\"")[1])

    #Ratings Section
    rating_list = []
    rating_list.append(review_raw.find(attrs={'itemprop':'ratingValue'})['content'])
    rating_list.append(review_raw.find(attrs={'itemprop':'description'})['content'])
    rating_list.append(review_raw.find(attrs={'itemprop':'reviewCount'})['content'])
    
    return(name,rating_list,info_list,image_list,room_type_list)

def main():
    hotelDetail('https://www.expedia.co.in/Raipur-Hotels-Hyatt-Raipur.h7065412.Hotel-Information?chkin=16/12/2019&chkout=17/12/2019&regionId=3033&destination=Raipur,+Chhattisgarh,+India&swpToggleOn=true&rm1=a2&x_pwa=1&trackingData=Cmp-wejY4k4JV22sZZUrBZm/jM4sYnQwYc1++xQAxmP9yqQ0CcwBjDAOu1DvHUcSDTu/rw66hA5lqXAuY0OlgVu2Wn6g99XPx5fF8fcl9+Pv3RS7Jl7d6RswGem6p8ZWZo3OODa0aX7D/dnxX4mQlHehJ+hLt+7o8gcSCwme5R4XwC8cl9bBALNYYhJ63kClS6EahFLuKhCKZgqSsEbETToa18UfXutbT85cSyIwudWTTCHT6NUz/W9OaT2WMc1gXlK1E+wBDfNSoOL/YTrxDc7p3nYrPwIwHpJT4jYYJypkDYQPJ+2RDxe1yLdcS+e+LBkdk9P7i3OkhER02m5eAOAzQQCGbuZTdR12KXwGwfO1/l54UXTfFCFIhku6drh1ujrjSyEPdtsJW8ZKcig2xxX0xfrMg4Bgc2kXruhATYSIpfIPNr0+tH37bIuwQaMOk4AY6e12xPI1DuLEBpGzMrPzLpMEu37f5kZDblw5wZYzX9fTDEzEeJzVCtft8n0DekPRe5hkNRvmX1Z3EoMQ0VMOH4MfEyQNoPqf9uTllr8/60ZiKRSnvBfpXbJ/IZOr2TiQM58QY+letcbPnpWLerI+TfR81WQYXU4mTFyEBNVsekBa2ydWHmwsb+1m9ocb3rkmeCoOTVQb8PCXcsClFAelOB0vPumMlZuhPgvqmNU1XRLmmmWYl3HRtEnoAtTDAnJTJtclqcJrIsAqPwOG0xxtj94y3yvfdI9Ffd4zJzsaFgafvuSCcz0Io2R7FRE0lGO+0JOzYjm9c2cBRpfBJRNhM31gO16rFTgqONWHgH38wcoyzvlJpbt1LYxhpu5ufLqNqBw6FbZgpyT2A803U2KZrFE613udHSsJ+qsoPIYGHU5GUiwtmix+eyu18WDbKCej2i7XW7Il48v0qUYh+hPnISmpxp1TZsD7aSA0YfhpI3r+bBYCHeE2P2MKU931HlD3I0YczAkf/aqZ0gGRZY/Ic4NIrB8SAi7+US4VjAEc7PnU9gpJoYZ84AxPBo5Fb0z+CedCEIT3rrYVKcknlk4lldJapTXqhGISg1mdm6oLuuQ=&rank=2&testVersionOverride=Buttercup,31936.93479.5,31844.87534.0,31779.89311.1,33090.94624.2,33131.92839.0&slots=HSR_AA&position=2&beaconIssued=2019-12-02T14:12:18&sort=recommended&top_dp=6250&top_cur=INR&rfrr=HSR&pwa_ts=1575295936192&referrerUrl=aHR0cHM6Ly93d3cuZXhwZWRpYS5jby5pbi9Ib3RlbC1TZWFyY2g=')
    # in_date = ['05','12','2019']
    # out_date = ['06','12','2019']
    # hotel_list = soupSite(getSource('Raipur',in_date,out_date,1,2))
    # # print(hotel_list)
    # with open('out.txt', 'w') as f:
    #     for item in hotel_list:
    #         f.write("%s\n" % item)
if __name__ == "__main__":
    main()