import requests
from bs4 import BeautifulSoup

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
    i = 0
    for list_ in soup.findAll('li', class_='listing uitk-cell xl-cell-1-1 l-cell-1-1 m-cell-1-1 s-cell-1-1'):
        list_data = list_.find('div', class_='uitk-card-content uitk-grid uitk-cell all-y-padding-three all-x-padding-three listing-content')
        # Content Scrape
        content = list_data.find('div', class_='uitk-cell all-cell-fill uitk-type-300')
            # Hotel Name
        name = content.h3.text
        local = content.div.text
            #Price
        price = list_data.find('div', class_='uitk-cell all-x-gutter-two uitk-type-right all-cell-shrink')
        price = price.div.div.find(attrs = {'data-stid':'content-hotel-lead-price'}).text.strip('Rs')
        review = list_data.find('div', class_='uitk-cell all-cell-align-bottom').find(attrs = {'data-stid':'content-hotel-review-info'})
            # Reviews
        rating = review.find(attrs = {'data-stid':'content-hotel-reviews-rating'}).text
        superlative = review.find(attrs = {'data-stid':'content-hotel-reviews-superlative'}).text
        total = review.find(attrs = {'data-stid':'content-hotel-reviews-total'}).text.strip('(  reviews)')
        reviews = {rating,superlative,total}

        # Image Scrape
        image_data = list_.find(class_='uitk-cell uitk-card-media')

        break
    

def main():
    in_date = ['01','12','2019']
    out_date = ['05','12','2019']
    soupSite(getSource('Delhi',in_date,out_date,1,2))

if __name__ == "__main__":
    main()