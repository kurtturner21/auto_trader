import requests
import json

# The secret key (SK) is required for this API call
TOKEN = 'pk_6b91a3125fbc4a1996832b2ed35a4798'
URL_BASE = 'https://cloud.iexapis.com/stable'      # production
END_POINT = '/stock/aapl/company'
R_URL = URL_BASE + END_POINT + '?token=' + TOKEN

r = requests.get(R_URL)
try:
    company_data = json.loads(r.text)
    with open('data\\company_data.txt', 'w') as fo:
        fo.write(json.dumps(company_data, indent=4, sort_keys=True))
except:
    print(r.text)

