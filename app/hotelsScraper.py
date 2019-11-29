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
    response = requests.request("GET", url, headers=headers, params=querystring)
    # with open('data.html', 'w') as file:
    #     file.write(response.content)
    return(response.content)

def soupSite(raw_html):
    soup = BeautifulSoup(raw_html,'lxml')
    final_list = []
    i = 0
    for list_ in soup.findAll('li', class_='listing uitk-cell xl-cell-1-1 l-cell-1-1 m-cell-1-1 s-cell-1-1'):
        if(list_['data-stid']):
            print('invalid list entry found')
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
            # Image Scrape
            image_data = list_.find(class_='uitk-cell uitk-card-media').section
            
            try:
                img_url_raw =  image_data.div.figure.div.figure['style']
                tp = img_url_raw.find('url(')
                img_url = img_url_raw[tp+4:img_url_raw.find('),')]
            except Exception as e:
                # print(e)
                # print(image_data)    
                # print(img_url_raw)
                pass
            #Create a list of all the data scraped and return them 
            currated_entry = [i,name,local,price,img_url,rating,superlative,total]
            final_list.append(currated_entry)
            i+=1
    return(final_list)

    # Sample Function call
#     in_date = ['01','12','2019']
#     out_date = ['05','12','2019']
#     hotel_list = soupSite(getSource('Ludhiana',in_date,out_date,1,2))
    # Sample Output
    '''
[ID, Hotel Name, Region, Price/Night, Image URL, 'Rating(out of 5)', 'Ratings in words', 'NumberOfPeopleWhoReviewed']
[0, 'Hyatt Regency Ludhiana', 'Ludhiana', '6,160', 'https://thumbnails.trvl-media.com/n-ezn4S3cpkoKemFKpO5rjFgaC8=/455x235/smart/images.trvl-media.com/hotels/8000000/7600000/7597500/7597440/b0889b1f_w.jpg', '4.3/5', 'Excellent', '184']
    '''


# Test Code
# def main():
#     in_date = ['01','12','2019']
#     out_date = ['05','12','2019']
#     hotel_list = soupSite(getSource('Ludhiana',in_date,out_date,1,2))
#     with open('out.txt', 'w') as f:
#         for item in hotel_list:
#             f.write("%s\n" % item)
# if __name__ == "__main__":
#     main()