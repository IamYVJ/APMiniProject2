import requests
import json
import os

base_url = 'https://apidojo-booking-v1.p.rapidapi.com/'
host = 'apidojo-booking-v1.p.rapidapi.com'
api_key = 'e665bf1174msh1acca6a2c3c99bfp165404jsn89b838b62158'

def getDestId(search_query):
    url = base_url + 'locations/auto-complete'
    querystring = {"languagecode":"en-us","text":search_query}

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': api_key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return(response.json()[0]['dest_id'])


def getDetails(dest_id,check_in,check_out,guest_qty,room_qty):
    url =  base_url + 'properties/list'

    c_in_str = check_in[2] + '-' + check_in[1] + '-' + check_in[0]
    c_out_str = check_out[2] + '-' + check_out[1] + '-' + check_out[0]
    print(c_in_str)
    print(c_out_str)
    breakpoint
    querystring = {"price_filter_currencycode":"INR","travel_purpose":"leisure",
                    "categories_filter":"price%3A%3A9-40%2Cfree_cancellation%3A%3A1%2Cclass%3A%3A1%2Cclass%3A%3A0%2Cclass%3A%3A2",
                    "search_id":"none","order_by":"popularity","children_qty":"2","languagecode":"en-us","children_age":"5%2C7",
                    "search_type":"city","offset":"0","dest_ids":"-3712125","guest_qty":guest_qty,
                    "arrival_date":c_in_str,"departure_date":c_out_str,"room_qty":room_qty}

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': api_key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open('list.json','w+') as js:
        js.write(json.dumps(response.json()))



def main():
    dest_id = getDestId('Ludhiana')
    check_in = ['01','12','2019']
    check_out = ['05','12','2019']
    getDetails(dest_id,check_in,check_out,2,1)

if __name__ == "__main__":
    main()