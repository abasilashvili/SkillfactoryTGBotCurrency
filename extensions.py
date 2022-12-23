import json
import requests
from config import exchanges


class APIException(Exception):
    pass


url = "https://api.apilayer.com/currency_data/change?start_date=23.12.2022&end_date=23.12.2022"

payload = {}
headers = {
    "apikey": "yGY23DriqRRJcZkxdiyGCw4HoAR14zjD"
}

response = requests.request("GET", url, headers=headers, data=payload)

status_code = response.status_code
result = response.text
