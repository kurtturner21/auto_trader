import requests
import json

# public key
TOKEN = 'Tpk_e710c58821a14b4e9ec672a324c3be3e'
#URL_BASE = 'https://cloud.iexapis.com/stable'      # production
URL_BASE = 'https://sandbox.iexapis.com/stable'     # for testing
END_POINT = '/stock/aapl/quote'
R_URL = URL_BASE + END_POINT + '?token=' + TOKEN

r = requests.get(R_URL)
quote_data = json.loads(r.text)
print(quote_data['companyName'], quote_data['latestPrice'])
with open('data\\stock_quote.txt', 'w') as fo:
    fo.write(json.dumps(quote_data, indent=4, sort_keys=True))


