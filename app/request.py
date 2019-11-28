import requests

url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/087550e2-b9e6-413c-9f5b-23abcb1581c2"

querystring = {"pageIndex":"0","pageSize":"10"}

headers = {
    'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
    'x-rapidapi-key': "f251de0f98msh616a56f76aa80abp10ca81jsn82b6415d9005"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)