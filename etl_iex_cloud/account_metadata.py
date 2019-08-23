import requests
import json

# The secret key (SK) is required for this API call
TOKEN = 'Tsk_0926ed355a89427ca3988aff1b858684'
#URL_BASE = 'https://cloud.iexapis.com/stable'      # production
URL_BASE = 'https://sandbox.iexapis.com/stable'     # for testing
END_POINT = '/account/metadata'
R_URL = URL_BASE + END_POINT + '?token=' + TOKEN

r = requests.get(R_URL)
account_data = json.loads(r.text)
with open('data\\account_metadata.txt', 'w') as fo:
    fo.write(json.dumps(account_data, indent=4, sort_keys=True))


