import requests
import json
import os

base_url = 'https://apidojo-booking-v1.p.rapidapi.com/'
host = 'apidojo-booking-v1.p.rapidapi.com'
api_key = 'e665bf1174msh1acca6a2c3c99bfp165404jsn89b838b62158'

def getList(search_query):
    url = base_url + 'locations/auto-complete'
    querystring = {"languagecode":"en-us","text":search_query}

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': api_key
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
     
    with open('hotels_list.json','w+') as js:
        js.write(json.dumps(response.json()))
    return(response.text)


# Driver Code
# def main():
#     getList('Ludhiana')

# if __name__ == "__main__":
#     main()