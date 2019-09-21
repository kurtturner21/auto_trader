import requests
import json

# public key
TOKEN = 'pk_6b91a3125fbc4a1996832b2ed35a4798'      # production
URL_BASE = 'https://cloud.iexapis.com/stable'      # production
# TOKEN = 'Tpk_e710c58821a14b4e9ec672a324c3be3e'     # for testing
# URL_BASE = 'https://sandbox.iexapis.com/stable'     # for testing
END_POINT = '/stock/aapl/news'
R_URL = URL_BASE + END_POINT + '?token=' + TOKEN


r = requests.get(R_URL)
try:
    stock_news_data = json.loads(r.text)
    print('stock_news_data len: ' + str(len(stock_news_data)))
    with open('data\\stock_news_data.txt', 'w') as fo:
        fo.write(json.dumps(stock_news_data, indent=4, sort_keys=True))
except:
    print(r.text)


