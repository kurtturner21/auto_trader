import os
import json
import csv
import hashlib
import sys
import requests
from datetime import datetime
from time import sleep
from time import gmtime
import time
import robin_stocks as rhood
import pandas as pd
import math

APP_BASE = os.path.join('c:' + os.sep, 'dev', 'auto_trader')
DATA_FILES_BASE = os.path.join('c:' + os.sep, 'auto_trader_data')
APP_CONFIG_DIR = os.path.join('c:' + os.sep, 'dev', 'auto_trader', 'etc')
APP_KILL_FILE = os.path.join('c:' + os.sep, 'dev', 'auto_trader', 'etc', 'delete_me_to_stop_app.kill_file.txt')

### compiled data
MONTHLY_FRAMES_PATH = os.path.join(DATA_FILES_BASE, 'monthly_frames')
HISTORY_PRICE_PATH = os.path.join(DATA_FILES_BASE, 'company_info')
COMPANY_INFO_PATH = os.path.join(DATA_FILES_BASE, 'company_info')
DOCUMENTS_DOWNLOAD_PATH = os.path.join(DATA_FILES_BASE, 'documents_stor')
DATA_PATH = os.path.join(DATA_FILES_BASE, 'stocks_lists.json')
DATA_PATH_TEST = os.path.join(DATA_FILES_BASE, 'stocks_lists_test.json')
AUTO_TRADER_CONFIG_PATH = os.path.join(DATA_FILES_BASE, 'etc', 'auto_trader_config.json')

### Robin hood
ROBIN_HOOD_CONFIG_PATH = os.path.join(DATA_FILES_BASE, 'etc', 'robin_hood_creds.json')
ROBIN_HOOD_URL_BASE_PROD = 'https://api.robinhood.com'      # production

### Last10K
LAST10K_CONFIG_PATH = os.path.join(DATA_FILES_BASE, 'etc', 'last10k_keys.json')
LAST10K_BASE = 'https://services.last10k.com'

### IEX
IEX_URL_BASE_PROD = 'https://cloud.iexapis.com/stable'      # production
IEX_URL_BASE_TEST = 'https://sandbox.iexapis.com/stable'     # for testing
IEX_TOKEN_PATHS = os.path.join(DATA_FILES_BASE, 'etc', 'iex_tokens.json')
IEX_ACCOUNT_METADATA = os.path.join(DATA_FILES_BASE,'etc', 'account_metadata.json')
IEX_UNKNOWN_SYMBOLS = os.path.join(DATA_FILES_BASE, 'etc', 'unkown_symbols.json')

### changing vars
date_code_latest = 19760101
idx_unknown_symbols = {}

### structrue
"""Symbol,Date,Open,High,Low,Close,Volume
E,01-Jan-2014,48.49,48.49,48.49,48.49,0
E,02-Jan-2014,47.72,47.72,47.23,47.32,232600
E,03-Jan-2014,47.64,47.91,47.47,47.74,251100
E,06-Jan-2014,48.05,48.35,47.92,48.1,442800
E,07-Jan-2014,47.92,48.3,47.76,48.3,220600
E,08-Jan-2014,47.74,47.9,47,47,327600
E,09-Jan-2014,47.55,47.59,46.91,46.99,123700"""

### auto trader config
app_config = {}
rb_config = {}
last10k_config = {}


def filter_me(stock_record):
    """
    This filter is designed to filter out some stocks that are lacking in data points
    """
    try:
        DESIRED_COUNTRIES_LIMIT = True
        DESIRED_COUNTRIES = ['US', 'AU', '', None]
        DESIRED_STOCK_ISSUE_TYPE_LIMIT = True
        DESIRED_STOCK_ISSUE_TYPE = ['ps','cs', 'ad', 'si']
        DESIRED_PRICE_BUCKET_LIMIT = True
        DESIRED_PRICE_BUCKET = ['deca', 'dollar','penny', 'half']
        NON_DESIRED_INDUSTRY_LIMIT = True
        NON_DESIRED_INDUSTRY = ['Precious Metals', 'Steel', 'Aluminum', 'Coal']
        MIN_HISTORY_LIMIT = True
        MIN_HISTORY = 200
        DIVIDEND_MIN_LIMIT = True
        DIVIDEND_MIN = .001
        PE_LIMIT = True
        PE_MAX = 1000
        PE_MIN = -5
        NEWS_LIMIT = False
        NEWS_MIN = 20
        RH_RATING_LIMIT = True
        RH_RATING_MIN = .9
        rh_rate_score = calculate_rating_score(stock_record)
        filter_me = False
        # if stock_record['iex_unknown_symbol']:
        #     filter_me = True
        if stock_record['country'] not in DESIRED_COUNTRIES and DESIRED_COUNTRIES_LIMIT:
            filter_me = True
        if stock_record['issueType'] not in DESIRED_STOCK_ISSUE_TYPE and DESIRED_STOCK_ISSUE_TYPE_LIMIT:
            filter_me = True
        if stock_record['price_bucket'] not in DESIRED_PRICE_BUCKET and DESIRED_PRICE_BUCKET_LIMIT:
            filter_me = True
        if 'h_count' in stock_record:
            if stock_record['h_count'] < MIN_HISTORY and MIN_HISTORY_LIMIT:
                filter_me = True
        else:
            filter_me = True
        if stock_record['industry'] in NON_DESIRED_INDUSTRY and NON_DESIRED_INDUSTRY_LIMIT:
            filter_me = True
        if stock_record['dividendYield'] < DIVIDEND_MIN and DIVIDEND_MIN_LIMIT:
            filter_me = True
        if (stock_record['peRatio'] < PE_MIN or stock_record['peRatio'] > PE_MAX) and PE_LIMIT:
            filter_me = True
        if stock_record['news_existing_ct'] < NEWS_MIN and NEWS_LIMIT:
            filter_me = True
        if rh_rate_score < RH_RATING_MIN and RH_RATING_LIMIT:
            filter_me = True
        return filter_me
    except:
        print('FAIL: this stock failed the filter_me process: ' + str(stock_record))
        sys.exit(20)


def filter_for_missing(stock_record):
    """
    This filter is designed to filter out some stocks that are lacking in data points
    """
    try:
        DESIRED_STOCK_ISSUE_TYPE_LIMIT = False
        DESIRED_STOCK_ISSUE_TYPE = ['ps','cs', 'ad', 'si']
        MAX_HISTORY_LIMIT = True
        MAX_HISTORY = 200
        filter_me = False
        if stock_record['issueType'] not in DESIRED_STOCK_ISSUE_TYPE and DESIRED_STOCK_ISSUE_TYPE_LIMIT:
            filter_me = True
        if stock_record['h_count'] > MAX_HISTORY:
            filter_me = True
        return filter_me
    except:
        print('FAIL: this stock failed the filter_for_missing process: ' + str(stock_record))
        sys.exit(20)


def filter_for_pulling_stock_histories(stock_record):
    """
    Include logic on what is the more disred stocks to keep up to date.
    """
    try:
        DESIRED_COUNTRIES_LIMIT = True
        DESIRED_COUNTRIES = ['US', 'AU', '', None]
        DESIRED_STOCK_ISSUE_TYPE_LIMIT = False
        DESIRED_STOCK_ISSUE_TYPE = ['ps','cs', 'ad', 'si']
        DIVIDEND_MIN_LIMIT = True
        DIVIDEND_MIN = .001
        filter_me = False
        if stock_record['country'] not in DESIRED_COUNTRIES and DESIRED_COUNTRIES_LIMIT:
            filter_me = True
        if stock_record['issueType'] not in DESIRED_STOCK_ISSUE_TYPE and DESIRED_STOCK_ISSUE_TYPE_LIMIT:
            filter_me = True
        if stock_record['dividendYield'] < DIVIDEND_MIN and DIVIDEND_MIN_LIMIT:
            filter_me = True
        return filter_me
    except:
        print('FAIL: this stock failed the filter_for_pulling_stock_histories process: ' + str(stock_record))
        sys.exit(20)


class sk_orders:
    def __init__(self):
        self.account = {
            'cash_deposits_total': 0,
            'cash': 0,
            'total_gain': 0,
            'ownership_days_agv': 0,
            'ct_owned': 0,
            'buffer': 0,
            'total_investments': 0,
            'trades': {'Sale': 0, 'Buy': 0}
        }
        self.order_history = []
        self.current_orders = {}
        self.options = {
            'show_each_transaction': True,
            'show_all_still_invested': True,
        }
        self.trans_logic_setting = {
            'MAX_LAST_LEN': 5,
            'AMT_OF_PROFIT': .01,
            'AMT_OF_PERCENT_CHANGE_TO_BUY': .2,
            'DAY_OF_PERCENT_GAIN': 30
        }
    def set_amt_of_profit_requried_to_sale(self, amt_of_profit):
        self.trans_logic_setting['AMT_OF_PROFIT'] = amt_of_profit
    def set_amt_of_percent_change_to_buy(self, amnt_of_percent):
        self.trans_logic_setting['AMT_OF_PERCENT_CHANGE_TO_BUY'] = amnt_of_percent
    def show_each_transaction(self):
        self.options['show_each_transaction'] = True
    def hide_each_transaction(self):
        self.options['show_each_transaction'] = False
    def show_all_still_invested(self):
        self.options['show_all_still_invested'] = True
    def hide_all_still_invested(self):
        self.options['show_all_still_invested'] = False
    def add_money(self, amount=0):
        self.account['cash'] += amount
        self.account['cash_deposits_total'] += amount
    def set_buffer(self, amount=0):
        self.account['buffer'] += amount
    def get_balance(self):
        return self.account['cash']
    def stock_logic_one(self, close_date, close_epoch, sk_symbol, stock_data):
        r_close = round(stock_data['Adj Close'], 2)
        r_nma= round(stock_data['nma'], 2)
        r_pct = round(stock_data['pct'], 2)
        if sk_symbol not in self.current_orders and r_close < r_nma and r_pct > self.trans_logic_setting['AMT_OF_PERCENT_CHANGE_TO_BUY']:
            if self.account['cash'] > (self.account['buffer'] + r_close):
                self.buy_stock(sk_symbol, r_close, close_epoch)
        elif sk_symbol in self.current_orders:
            s_invested = self.current_invested(sk_symbol)
            s_profit = self.current_profit(sk_symbol, r_close)
            if s_profit > (s_invested * self.trans_logic_setting['AMT_OF_PROFIT']):
                self.sale_stock(sk_symbol, r_close, close_epoch)
    def buy_stock(self, sk, buy_price, purchase_epoch):
        share_count = int((
            self.account['cash']*.5 - self.account['buffer']
            ) / buy_price)
        proposed_total = round(share_count * buy_price, 2)
        if share_count > 10:
            self.account['trades']['Buy'] += 1
            self.current_orders.update({sk:
                    {
                    'sk': sk, 
                    'purchase_price': buy_price,
                    'purchase_epoch': purchase_epoch,
                    'sale_epoch': None,
                    'ownership_len': 0,
                    'share_count': share_count,
                    'sale_price': None,
                    'profit': None
                }})
            self.account['cash'] = round(
                self.account['cash'] - (self.current_orders[sk]['share_count'] * buy_price), 2)
            if self.options['show_each_transaction']:
                print('{0:<10} {1:<5} $:{2:<10} ct:{3:<10}  PURCHASE                              inv: {4}'.format(
                    epoch_to_human(purchase_epoch), 
                    sk, buy_price, share_count, proposed_total))
    def sale_stock(self, sk, sale_price, sale_epoch):
        self.account['trades']['Sale'] += 1
        self.account['cash'] = round(
            self.account['cash'] + (self.current_orders[sk]['share_count'] * sale_price), 2)
        self.current_orders[sk]['sale_epoch'] = sale_epoch
        self.current_orders[sk]['ownership_len'] = math.ceil(
                (self.current_orders[sk]['sale_epoch'] - self.current_orders[sk]['purchase_epoch'])/3600/24)
        self.current_orders[sk]['sale_price'] = round(sale_price, 2)
        self.current_orders[sk]['profit'] = round((sale_price - self.current_orders[sk]['purchase_price']) * self.current_orders[sk]['share_count'], 2)
        if self.options['show_each_transaction']:
            print('{0:<10} {1:<5} $:{2:<10} ct:{3:<10}  SALE    Profit:  {4:<10}   len:{5:<3}'.format(
                epoch_to_human(sale_epoch), 
                sk, sale_price, 
                self.current_orders[sk]['share_count'], 
                self.current_orders[sk]['profit'],
                self.current_orders[sk]['ownership_len'])
                )
        self.order_history.append(self.current_orders.pop(sk))

    def current_profit(self, sk, sale_price):
        return round((sale_price - self.current_orders[sk]['purchase_price']) * self.current_orders[sk]['share_count'], 2)
    def current_invested(self, sk):
        share_count = self.current_orders[sk]['share_count']
        purchase_price = self.current_orders[sk]['purchase_price']
        return round((share_count * purchase_price), 2)
    def current_investment_prt(self, close_epoch=datetime.now().timestamp(), mount_count=''):
        print('\n {0:<5} current investments {1:<20}'.format(mount_count, epoch_to_human(close_epoch)))
        total_investments = 0
        total_len_ownership = 0
        ct_owned = 0
        for sk in sorted(self.current_orders):
            ct_owned += 1
            share_count = self.current_orders[sk]['share_count']
            purchase_price = self.current_orders[sk]['purchase_price']
            ownership_days = math.ceil((close_epoch - self.current_orders[sk]['purchase_epoch'])/3600/24)
            total_len_ownership += ownership_days
            invested = round((share_count * purchase_price), 2)
            total_investments += invested
            profit = '' #round((sale_price - self.current_orders[sk]['purchase_price']) * self.current_orders[sk]['share_count'], 2)
            if self.options['show_all_still_invested']:
                print('\tstock:{0:<5} ct:{1:<5} profit:{2:<10} invested:{3:<10} days:{4:<4}  Still invested...'.format(
                    sk, share_count, profit, invested, ownership_days))
        total_gain = round(total_investments + self.account['cash'] - self.account['cash_deposits_total'], 2)
        if ct_owned:
            ownership_days_agv = round(total_len_ownership / ct_owned, 2)
        else:
            ownership_days_agv = 0
        self.account['total_gain'] = total_gain
        self.account['ownership_days_agv'] = ownership_days_agv
        self.account['ct_owned'] = ct_owned
        self.account['total_investments'] = round(total_investments,2)
        print('\ttotal deposits: {0:<20}     total_gain: {1:<10}   ownership_days_agv: {2:<5}  ct_owned:{3:<2}'.format(
            self.account['cash_deposits_total'], total_gain, ownership_days_agv, ct_owned))
        print('\ttotal_investments: {0:<20}  cash: {1:<18} trades: {2:<20}'.format(
            round(total_investments,2), self.account['cash'], str(self.account['trades'])))
    def order_history_prt(self):
        print('\norder history:')
        for oh in self.order_history:
            share_count = oh['share_count']
            purchase_price = oh['purchase_price']
            ownership_days = oh['ownership_len']
            invested = round((share_count * purchase_price), 2)
            profit = oh['profit']
            print('\tstock:{0:<5} ct:{1:<5} profit:{2:<10} invested:{3:<10} days:{4:<4}'.format(oh['sk'], share_count, profit, invested, ownership_days))
        

#####
# print constructors
#####
def printing_stock_standard(loop_num, stock_record, print_standard='one'):
    rh_rate_score = calculate_rating_score(stock_record)
    if print_standard == 'one':
        stock_row_print_format = '{0:<6}{1:<10}{2:<10}{3:<10}{4:<30}{5:<10}{6:<30}{7:<25}{8:<5}{9:<5}{10:<8}{11:<10} n:{12:<10} r:{13:<3}'
        print_str = stock_row_print_format.format(loop_num, stock_record['symbol'], stock_record['h_close'], stock_record['h_count'], 
            stock_record['companyName'][:28].encode("ascii", 'ignore').decode("ascii"), stock_record['employees'], stock_record['industry'][:28], 
            stock_record['sector'][:23], stock_record['issueType'], 
            stock_record['country'], stock_record['peRatio'], stock_record['dividendYield'], stock_record['news_existing_ct'],
            rh_rate_score
            )
        print(print_str)
    elif print_standard == 'two':
        stock_record['dividendYield']
        stock_row_print_format = '{0:<6}{1[symbol]:<5}{1[issueType]:<8}{1[country]:<10}{1[peRatio]:<10}{1[dividendYield]:<10} rating:{2:<3}'
        print_str = stock_row_print_format.format(loop_num, stock_record, rh_rate_score)
        print(print_str)


def calculate_rating_score(stock_record):
    rh_rate_score_divisor = (stock_record['rh_buy'] + stock_record['rh_hold'] + stock_record['rh_sell'])
    if rh_rate_score_divisor > 0 and stock_record['rh_error_code'] == 0:
        rh_rate_score = round(((stock_record['rh_buy'] * 1 + stock_record['rh_hold'] * .5 + stock_record['rh_sell'] * 0) /  rh_rate_score_divisor), 2)
    else:
        rh_rate_score = .2
    return rh_rate_score


def print_process_module_status(module_name, this_stime, overall_stime):
    print('Time to process {0:<30} this: {1:<20}  overall: {2:<20}'.format(
            module_name,
            round(datetime.now().timestamp() - this_stime, 2), 
            round(datetime.now().timestamp() - overall_stime, 2)
            ))



def print_stock_news(stock_symbol):
    print('\t### NEWS')
    news_items = iex_get_exising_news_items(stock_symbol)
    for ni_k_ct, ni_k in enumerate(sorted(news_items)):
        if ni_k_ct < 10:
            news_item = news_items[ni_k]
            print('\t' + epoch_to_human(news_item['datetime']) + '\t' +
                news_item['headline'].encode("ascii", 'ignore').decode("ascii") + '\t' +
                news_item['related']
                )


def print_stock_history(stock_symbol, days_into_past=10, to_reverse=True):
    print('\t### History')
    st_history_data = stock_history_load(stock_symbol)
    for sk_h_ct, sk_h in enumerate(sorted(st_history_data['history_data'], reverse=to_reverse)):
        if sk_h_ct < 10:
            print(sk_h, st_history_data['history_data'][sk_h])


#####
# date time methods
#####


def find_hours_since_epoch(last_epoch):
    epoch_now = float(datetime.now().timestamp())
    try:
        last_epoch_float = float(last_epoch)
    except:
        last_epoch_float = 0.0
    return round(float(epoch_now - float(last_epoch_float))/60/60, 6)


def generate_effective_epoch():
    return datetime.timestamp(datetime.now())


def generate_effective_string():
    return str(datetime.now())


def epoch_to_human(epoch_time, str_format='%m/%d/%Y %H:%M:%S'):
    epoch_time_float = float(epoch_time)
    if len(str(int(epoch_time_float))) == 10:
        return time.strftime(str_format,  gmtime(epoch_time_float))
    else:
        return time.strftime(str_format,  gmtime(epoch_time_float/1000.))


def human_to_epoch(human_time, str_format='%Y-%m-%d %H:%M:%S'):
    """
    expected format: '%Y-%m-%d %H:%M:%S'  STRING
    example: 2019-10-11 00:00:00
    """
    return datetime.strptime(human_time, str_format).timestamp()


#####
# data objects
#####
def create_stock_lists_stock(sk_symbol):
    return {
        "companyName": "",
        "exchange": "",
        "iex_company_info_path": "",
        "iex_company_info_effect_epoch": 0,
        "iex_news_epoch": 0,
        "price_bucket": "",
        "industry": "",
        "h_source": "",
        "tags": [],
        "sector": "",
        "country": "",
        "issueType": "",
        "employees": 0,
        "dividendYield": 0.0,
        "symbol": sk_symbol
    }


def create_rating_object():
    return {
        "buy": 0,
        "sell": 0,
        "hold": 0,
        "last_rh_api_epoch": 0,
        "new_ratings_count": 0,
        "hash_list": [],
        "ratings": {},
        "error_code": 0
    }


def create_empty_stock_history():
    # dt = datetime.today()
    # index = pd.date_range(dt, periods=0, freq='D')
    columns = ['Date','High','Low','Open','Close','Volume','Adj Close']
    df_ = pd.DataFrame(columns=columns)
    df_ = df_.set_index('Date')
    df_ = df_.fillna(0) # with 0s rather than NaNs
    return df_


#####
# LAST10k functions
#####

def last10k_load_key():
    last10k_key = {}
    if os.path.isfile(LAST10K_CONFIG_PATH):
        with open(LAST10K_CONFIG_PATH, "r") as fi:
            last10k_key = json.load(fi)
    else:
        print('file not found', LAST10K_CONFIG_PATH)
    return last10k_key['key']



def last10k_cik(this_sk_symbol):
    last10k_key = last10k_load_key()
    end_point = '/v1/company/'
    end_point = '/v1/company/{0}/cik'.format(this_sk_symbol.upper())
    headers = {'Ocp-Apim-Subscription-Key': last10k_key}
    r_url = LAST10K_BASE + end_point
    r = requests.get(r_url, headers=headers)
    try:
        return json.loads(r.text)
    except:
        print("WARNING LAST10K CIK CALL FAILED!!!", this_sk_symbol)
        return 0


#####
# robin hood fuctions
#####

def r_login():
    global rb_config
    robin_hood_config_file_load()
    return rhood.authentication.login(rb_config['un'], rb_config['pw'])


def r_logout():
    robin_hood_config_file_save()
    rhood.authentication.logout()


def r_get_portfolio_profile():
    profile = rhood.profiles.load_portfolio_profile()
    return profile


# def r_get_account_documents():
#     return rhood.account.get_documents()

# def r_get_account_download_document(url, name, dirpath, fileext='pdf'):
#     r = requests.get(url)
#     f_path = os.path.join(dirpath, name)  + '.' + fileext
#     with open(f_path, 'wb') as fo:
#         fo.write(r.content)
#     # profile = rhood.account.download_document(url, name, dirpath)


def r_get_build_user_profile():
    profile = rhood.account.build_user_profile()
    return profile


def r_get_bank_transfers():
    profile = rhood.account.get_bank_transfers()
    return profile


def r_get_stock_earnings(sk_symbol):
    stock_earnings = rhood.stocks.get_earnings(sk_symbol)
    return stock_earnings


def r_get_stock_fundamentals(sk_symbol):
    stock_fundamentals = rhood.stocks.get_fundamentals(sk_symbol)
    return stock_fundamentals


def r_get_stock_events(sk_symbol):
    stock_events = rhood.stocks.get_events(sk_symbol)
    return stock_events


def r_get_stock_popularity(sk_symbol):
    stock_popularity = rhood.stocks.get_popularity(sk_symbol)
    return stock_popularity


def r_get_ratings(sk_symbol):
    ratings_data_path = define_stock_rh_ratings(sk_symbol)
    make_dir_if_not_exists(ratings_data_path)
    if os.path.isfile(ratings_data_path):
        with open(ratings_data_path, "r") as fi:
            ratings_data = json.load(fi)  
        ### only needed temporary 
        if 'returned_ct' in ratings_data:
            ratings_data = kill_dict_key(ratings_data, 'returned_ct')
        if 'last_rb_api_epoch' in ratings_data:
            ratings_data.update({'last_rh_api_epoch': ratings_data['last_rb_api_epoch']})
            ratings_data = kill_dict_key(ratings_data, 'last_rb_api_epoch')
    else:
        # print('\t\tnew ratings file ' +  ratings_data_path)
        ratings_data = create_rating_object()
    new_epoch =  generate_effective_epoch()
    try:
        sk_rates = rhood.stocks.get_ratings(sk_symbol)
        new_ratings_count = 0
        ratings_data['last_rh_api_epoch'] = new_epoch
        if 'ratings' in sk_rates:
            ### these number rarly match the text versions
            if 'summary' in sk_rates:
                if sk_rates['summary']:
                    ratings_data['sell'] = sk_rates['summary']['num_sell_ratings']
                    ratings_data['buy'] = sk_rates['summary']['num_buy_ratings']
                    ratings_data['hold'] = sk_rates['summary']['num_hold_ratings']
                    ratings_data['error_code'] = 0
                else:
                    ratings_data['error_code'] = 2
            for rate in sk_rates['ratings']:
                r_text = rate['text'].decode('utf-8', 'ignore').encode('utf-8')
                r_hash = hashlib.md5(r_text).hexdigest()
                r_key = str(new_epoch) + '_' + r_hash
                r_type = rate['type']
                if r_hash not in ratings_data['hash_list']:
                    new_ratings_count += 1
                    ratings_data['hash_list'].append(r_hash)
                    ratings_data['ratings'].update({r_key: {
                        'type': r_type, 
                        'text': r_text.decode('ascii', 'ignore')
                        }})
            ratings_data['new_ratings_count'] = new_ratings_count
    except:
        ratings_data['error_code'] = 1
    with open(ratings_data_path, 'w') as fo:
        fo.write(json.dumps(ratings_data, indent=4, sort_keys=True))
    return ratings_data


#####
# IEX
#####
def iex_load_tokens():
    iex_tokens = {}
    if os.path.isfile(IEX_TOKEN_PATHS):
        with open(IEX_TOKEN_PATHS, "r") as fi:
            iex_tokens = json.load(fi)
    else:
        print('file not found', IEX_TOKEN_PATHS)
    return iex_tokens



def iex_symbols():
    iex_tokens = iex_load_tokens()
    end_point = '/ref-data/symbols'
    r_url = IEX_URL_BASE_PROD + end_point + '?token=' + iex_tokens['production_secret'] 
    try:
        r = requests.get(r_url)
        symbols = json.loads(r.text)
        return symbols
    except:
        print("WARNING IEX SYMBOLS CALL FAILED!!!")



def iex_account_metadata_display():
    iex_tokens = iex_load_tokens()
    end_point = '/account/metadata'
    r_url = IEX_URL_BASE_PROD + end_point + '?token=' + iex_tokens['production_secret']
    r = requests.get(r_url)
    try:
        account_data = json.loads(r.text)
        with open(IEX_ACCOUNT_METADATA, 'w') as fo:
            fo.write(json.dumps(account_data, indent=4, sort_keys=True))
        messagesUsed = int(account_data['messagesUsed'])
        messageLimit = int(account_data['messageLimit'])
        messageRemain = messageLimit - messagesUsed
        print('IEX digits     messageLimit: {0:<12}  messagesUsed: {1:<12}  messageRemain: {2:<12}'.format(
            messageLimit, messagesUsed, messageRemain
        ))
    except:
        print(r.text)


def iex_stock_key_facts_fix(key_facts):
    if 'peRatio' not in key_facts:
        key_facts.update({'peRatio': 0.0})
    if key_facts['peRatio'] in ['', 'None', None]:
        key_facts.update({'peRatio': 0.0})
    if 'dividendYield' not in key_facts:
        key_facts.update({'dividendYield': 0.0})
    if key_facts['dividendYield'] in ['', 'None', None]:
        key_facts.update({'dividendYield': 0.0})
    else:
        key_facts.update({'dividendYield': round(float(key_facts['dividendYield']), 4)})
    return key_facts



def iex_stock_get_key_facts(sk_symbol):
    """
    The update logic will be managed by this method. 
    """
    def call_iex(this_sk_symbol):
        iex_tokens = iex_load_tokens()
        end_point = '/stock/{0}/stats'.format(this_sk_symbol)
        r_url = IEX_URL_BASE_PROD + end_point + '?token=' + iex_tokens['production_secret']
        r = requests.get(r_url)
        key_facts = {}
        is_unknown_symbol = False
        try:
            key_facts = json.loads(r.text)
            key_facts = iex_stock_key_facts_fix(key_facts)
        except:
            if 'Unknown symbol' in r.text:
                iex_unknown_symbols_add(this_sk_symbol)
            print(r.text)
            is_unknown_symbol = True
        return key_facts, is_unknown_symbol
    def write_key_facts(all_key_facts_data, all_key_facts_data_path):
        """ assumes that epochs will be dates """
        with open(all_key_facts_data_path, 'w') as fo:
            fo.write(json.dumps(all_key_facts_data, indent=4, sort_keys=True))
    ### declares
    HOURS_BETWEEN_IEX_KEY_FACTS = get_hours_between_iex_key_facts()
    global idx_unknown_symbols
    api_call = False
    is_unknown_symbol = False
    key_facts = {}
    key_fact_data_path = define_stock_iex_key_facts(sk_symbol)
    make_dir_if_not_exists(key_fact_data_path)
    latest_epoch = str(generate_effective_epoch())
    ### what do do
    if sk_symbol in idx_unknown_symbols:
        """ know unknown file """
        key_facts = iex_stock_key_facts_fix({})
        return {'data': key_facts, 'latest_epoch': 0, 'api_call': False, 'unknown_symbol': True}
    if not os.path.isfile(key_fact_data_path):
        """ data file does not exists, call api, make file """
        api_call = True
        key_facts, is_unknown_symbol = call_iex(sk_symbol)
        key_facts = iex_stock_key_facts_fix(key_facts)      ### got to fix and clean
        write_key_facts({latest_epoch : key_facts}, key_fact_data_path)
        print('Writing key facts for the first time for ' + sk_symbol + ' here ' + key_fact_data_path)
    else:
        """ data file DOES exist, open, check epoch, supply existing or pull new """
        all_key_facts_data = {}
        with open(key_fact_data_path, "r") as fi:
            all_key_facts_data = json.load(fi)
        latest_epoch_in_file = sorted(all_key_facts_data.keys())[-1]
        ### within the limit:
        if HOURS_BETWEEN_IEX_KEY_FACTS > find_hours_since_epoch(latest_epoch_in_file): 
            key_facts = iex_stock_key_facts_fix(all_key_facts_data[latest_epoch_in_file])
            latest_epoch = latest_epoch_in_file
        else:
            api_call = True
            key_facts, is_unknown_symbol = call_iex(sk_symbol)
            key_facts = iex_stock_key_facts_fix(key_facts)      ### got to fix and clean
            all_key_facts_data.update({latest_epoch : key_facts})
            write_key_facts(all_key_facts_data, key_fact_data_path)
            print('updated an existing key facts file for ' + sk_symbol + ' here ' + key_fact_data_path) 
    return {
        'data': key_facts,
        'api_call': api_call,
        'unknown_symbol': is_unknown_symbol,
        'latest_epoch': latest_epoch
        }


def iex_stock_news_get(sk_symbol):
    ### NOT FINISHED
    def call_iex(this_sk_symbol):
        iex_tokens = iex_load_tokens()
        end_point = '/stock/{0}/news/last/100'.format(this_sk_symbol)
        r_url = IEX_URL_BASE_PROD + end_point + '?token=' + iex_tokens['production_secret']
        r = requests.get(r_url)
        my_news = {}
        is_unknown_symbol = False
        try:
            my_news = json.loads(r.text)
        except:
            if 'Unknown symbol' in r.text:
                iex_unknown_symbols_add(this_sk_symbol)
            print(r.text)
            is_unknown_symbol = True
        return my_news, is_unknown_symbol
    def write_news(all_news_data, all_news_data_path):
        """ assumes that epochs will be dates """
        with open(all_news_data_path, 'w') as fo:
            fo.write(json.dumps(all_news_data, indent=4, sort_keys=True))
    global idx_unknown_symbols
    news_new_count = 0
    news_returned_count = 0
    news_oldest_item_epoch_in_set = 0
    if sk_symbol in idx_unknown_symbols:
        return {'news_new_count': 0, 'news_existing_ct': 0, 'news_oldest_item_epoch_in_set': 0, 'news_returned_count': '', 'api_call': False, 'unknown_symbol': True}
    news_path = define_stock_iex_news(sk_symbol)
    make_dir_if_not_exists(news_path)
    existing_news = iex_open_news(news_path)
    news_existing_ct = len(existing_news)
    new_news, is_unknown_symbol = call_iex(sk_symbol)
    if not is_unknown_symbol:
        for n_item in new_news:
            news_returned_count += 1
            if news_oldest_item_epoch_in_set > n_item['datetime'] or news_oldest_item_epoch_in_set == 0:
                news_oldest_item_epoch_in_set = n_item['datetime']
            n_key = str(n_item['datetime']) + '_' + make_news_hash_of_list(n_item)
            if n_key not in existing_news:
                news_new_count += 1
                existing_news.update({n_key: n_item})
        write_news(existing_news, news_path)
    return {
        'news_new_count': news_new_count,
        'news_returned_count': news_returned_count,
        'news_existing_ct': news_existing_ct,
        'news_oldest_item_epoch_in_set': news_oldest_item_epoch_in_set,
        'api_call': True,
        'unknown_symbol': is_unknown_symbol
    }
    

def iex_get_exising_news_item_count(sk_symbol):
    """
    Returns the number of entries in the stock news file. 
    """
    news_path = define_stock_iex_news(sk_symbol)
    existing_news = iex_open_news(news_path) 
    news_existing_ct = len(existing_news)
    return news_existing_ct


def make_news_hash_of_list(n_item):
    """
    ONLY FOR NEWS ITEMS.
    """
    to_b_hashed_str = ''
    for k in sorted(n_item):
        to_b_hashed_str += str(n_item[k])
    return hashlib.md5(to_b_hashed_str.encode('utf-8')).hexdigest()


def iex_get_exising_news_items(sk_symbol):
    """
    Returns a list of news items from file with sk_symbol.
    """
    news_path = define_stock_iex_news(sk_symbol)
    existing_news = iex_open_news(news_path)
    return existing_news


def iex_open_news(all_news_data_path):
    """
    Returns a list of news items from file with path to news file.
    """
    news_data = {}
    if os.path.isfile(all_news_data_path):
        with open(all_news_data_path, "r") as fi:
            news_data = json.load(fi)
    return news_data


def iex_stock_company_fix_info(company_data):
    if 'employees' not in company_data:
        company_data.update({'employees': 0})
    if not company_data['employees']:
        company_data['employees'] = 0
    if 'tags' not in company_data:
        company_data.update({'tags': []})
    if 'industry' not in company_data:
        company_data.update({'industry': ''})
    if 'sector' not in company_data:
        company_data.update({'sector': ''})
    if 'issueType' not in company_data:
        company_data.update({'issueType': ''})
    if 'country' not in company_data:
        company_data.update({'country': ''})
    if not company_data['country']:
        company_data.update({'country': ''})
    return company_data


def iex_stock_company_get_info(sk_symbol, pull_new_data=False):
    """
    If pull_new_data is True, then it will pull from the API.
    If pull_new_data is False, then it will pull from the file. 
    So update logic is desigend by the calling application.  
    """
    global idx_unknown_symbols
    api_call = False
    if sk_symbol in idx_unknown_symbols:
        return {'data': {}, 'file_path': '', 'api_call': False, 'unknown_symbol': True}
    company_data_path = define_stock_iex_company_info(sk_symbol)
    make_dir_if_not_exists(company_data_path)
    if not os.path.isfile(company_data_path) or pull_new_data:
        api_call = True
        iex_tokens = iex_load_tokens()
        end_point = '/stock/{0}/company'.format(sk_symbol)
        r_url = IEX_URL_BASE_PROD + end_point + '?token=' + iex_tokens['production_secret']
        r = requests.get(r_url)
        company_data = {}
        try:
            company_data = json.loads(r.text)
            company_data = iex_stock_company_fix_info(company_data)
            with open(company_data_path, 'w') as fo:
                fo.write(json.dumps(company_data, indent=4, sort_keys=True))
        except:
            if 'Unknown symbol' in r.text:
                iex_unknown_symbols_add(sk_symbol)
            print(r.text)
    else:
        with open(company_data_path, "r") as fi:
            company_data = json.load(fi)
        company_data = iex_stock_company_fix_info(company_data)
    return {
        'data': company_data,
        'file_path': company_data_path,
        'api_call': api_call,
        'unknown_symbol': False
        }


def iex_unknown_symbols_add(sk_symbol):
    global idx_unknown_symbols
    if sk_symbol not in idx_unknown_symbols:
        idx_unknown_symbols.update({
            sk_symbol: generate_effective_epoch()
            })
        with open(IEX_UNKNOWN_SYMBOLS, 'w') as fo:
            fo.write(json.dumps(idx_unknown_symbols, indent=4, sort_keys=True))


def iex_unknown_symbols_load():
    global idx_unknown_symbols
    if os.path.isfile(IEX_UNKNOWN_SYMBOLS):
        with open(IEX_UNKNOWN_SYMBOLS, "r") as fi:
            idx_unknown_symbols = json.load(fi)
    print('IEX unknown loaded:', len(idx_unknown_symbols))


def iex_issue_type_code(issue_type):
    """refers to the common issue type of the stock."""
    ### An ADR stock or ADS is a foreign stock that allows U.S. investors to trade its shares on a U.S. exchange.
    if issue_type == 'ad':
        return 'American Depository Receipt (ADR\'s)'
    ### Equity REITs is the most common form of enterprise. These entities buy, own and manage income-producing real estate. Revenues come primarily through rents and not from the reselling of the portfolio properties. Mortgage REITs, also known as mREITs, lend money to real estate owners and operators
    elif issue_type == 're':
        return 'Real Estate Investment Trust (REIT\'s)'
    elif issue_type == 'ce':
        return 'Closed end fund (Stock and Bond Fund)'
    ### There are two types of secondary offerings. A non-dilutive secondary offering is a sale of securities in which one or more major stockholders in a company sell all or a large portion of their holdings. ... Meanwhile, a dilutive secondary offering involves creating new shares and offering them for public sale.
    elif issue_type == 'si':
        return 'Secondary Issue'
    elif issue_type == 'lp':
        return 'Limited Partnerships'
    elif issue_type == 'cs':
        return 'Common Stock'
    ###An exchange-traded fund (ETF) is a collection of securities—such as stocks—that tracks an underlying index. The best-known example is the SPDR S&P 500 ETF (SPY), which tracks the S&P 500 Index. ETFs can contain many types of investments, including stocks, commodities, bonds, or a mixture of investment types. An exchange-traded fund is a marketable security, meaning it has an associated price that allows it to be easily bought and sold.
    elif issue_type == 'et':
        return 'Exchange Traded Fund (ETF)'
    elif issue_type == 'wt':
        return 'Warrant'
    elif issue_type == 'rt':
        return 'Right'
    elif issue_type == 'oef':
        return 'Open Ended Fund'
    elif issue_type == 'cef':
        return 'Closed Ended Fund'
    elif issue_type == 'ps':
        return 'RiPreferred Stockght'
    else:
        return 'Not-Mapped'


#####
# config getters & setters
####

def get_last_time_ran():
    global app_config
    return app_config['last_time_ran']

def set_last_time_ran(last_time_ran):
    global app_config
    app_config['last_time_ran'] = last_time_ran
    auto_traider_config_file_save()

def set_last10k_api_count_current(count):
    global app_config
    app_config['last10k_api_count_current'] = count
    auto_traider_config_file_save()

def get_last10k_api_count_current():
    global app_config
    return app_config['last10k_api_count_current']

def get_last10k_api_count_max():
    global app_config
    return app_config['last10k_api_count_max']

def set_last10k_api_count_month(month_code):
    global app_config
    app_config['last10k_api_count_month'] = month_code
    auto_traider_config_file_save()

def get_last10k_api_count_month():
    global app_config
    return app_config['last10k_api_count_month']


def get_hours_to_collect_news_for_zeros():
    global app_config
    return app_config['hours_to_collect_news_for_zeros']


def get_run_in_testing():
    global app_config
    return app_config['run_in_testing']


def get_sleep_time_out_on_iex():
    global app_config
    return app_config['sleep_time_out_on_iex']


def get_hours_between_iex_comp_info():
    global app_config
    return app_config['hours_between_iex_comp_info']


def get_hours_between_iex_key_facts():
    global app_config
    return app_config['hours_between_iex_key_facts']


def get_hours_between_history_close_dates():
    global app_config
    return app_config['hours_between_history_close_dates']


#####
# file based methods
#####

def auto_traider_config_file_save():
    global app_config
    with open(AUTO_TRADER_CONFIG_PATH, 'w') as fo:
        json.dump(app_config, fo, sort_keys=True, indent=4)


def auto_traider_config_file_load():
    global app_config
    if os.path.isfile(AUTO_TRADER_CONFIG_PATH):
        with open(AUTO_TRADER_CONFIG_PATH, "r") as fi:
            app_config = json.load(fi)


def robin_hood_config_file_save():
    global rb_config
    with open(ROBIN_HOOD_CONFIG_PATH, 'w') as fo:
        json.dump(rb_config, fo, sort_keys=True, indent=4)


def robin_hood_config_file_load():
    global rb_config
    if os.path.isfile(ROBIN_HOOD_CONFIG_PATH):
        with open(ROBIN_HOOD_CONFIG_PATH, "r") as fi:
            rb_config = json.load(fi)


def kill_file_touch():
    make_dir_if_not_exists(APP_KILL_FILE)
    if not os.path.isfile(APP_KILL_FILE):
        with open(APP_KILL_FILE, 'w') as fo:
            fo.write('Delete this file to stop application nicely.')


def kill_file_check():
    do_exit = True
    if os.path.isfile(APP_KILL_FILE):
        do_exit = False
    else:
        print('Kill file missing - send flag to do_exit!!!')
    return do_exit

def define_stock_iex_key_facts(sk):
    return os.path.join(COMPANY_INFO_PATH, sk[:1].lower(), '_' + sk.lower() + '_iex_key_facts.json')

def define_stock_iex_news(sk):
    return os.path.join(COMPANY_INFO_PATH, sk[:1].lower(), '_' + sk.lower() + '_news.json')

def define_stock_iex_company_info(sk):
    return os.path.join(COMPANY_INFO_PATH, sk[:1].lower(), '_' + sk.lower() + '_iex_compnay_info.json')

def define_stock_rh_ratings(sk):
    return os.path.join(COMPANY_INFO_PATH, sk[:1].lower(), '_' + sk.lower() + '_rh_ratings.json')

def define_stock_hist_path(sk):
    return os.path.join(HISTORY_PRICE_PATH, sk[:1].lower(), '_' + sk.lower() + '.csv')

def define_monthly_frames_history_path(yyyy_mm_code):
    return os.path.join(MONTHLY_FRAMES_PATH, yyyy_mm_code + '.csv')

def define_monthly_eval_report_path():
    return os.path.join(MONTHLY_FRAMES_PATH, 'report.csv')

def get_stock_symbol_from_path(st_path):
    return os.path.basename(st_path)[1:].split('.')[0]

def get_document_stor_account_statements():
    return os.path.join(DOCUMENTS_DOWNLOAD_PATH, 'account_statements')

def get_document_stor_trade_confirm():
    return os.path.join(DOCUMENTS_DOWNLOAD_PATH, 'trade_confirm')


def make_dir_if_not_exists(file_path):
    dir_path = os.path.dirname(file_path)
    isD = os.path.isdir(dir_path)
    if not isD:
        os.makedirs(dir_path)
        print('made directory:', dir_path)


def stock_data_file_save(stocks):
    with open(DATA_PATH, 'w') as fo:
        json.dump(stocks, fo, sort_keys=True, indent=4)
    print('Stocks saved:', len(stocks))


def stock_data_file_load():
    stocks = {}
    if os.path.isfile(DATA_PATH):
        with open(DATA_PATH, "r") as fi:
            stocks = json.load(fi)
    print('Stocks loaded:', len(stocks))
    return stocks


def test_stock_data_file_save(stocks):
    with open(DATA_PATH_TEST, 'w') as fo:
        json.dump(stocks, fo, sort_keys=True, indent=4)
    print('Stocks saved:', len(stocks))


def test_stock_data_file_load():
    stocks = {}
    if os.path.isfile(DATA_PATH_TEST):
        with open(DATA_PATH_TEST, "r") as fi:
            stocks = json.load(fi)
    print('Stocks loaded:', len(stocks))
    return stocks


def list_all_stock_histories():
    full_paths = []
    for root, dirs, files in os.walk(HISTORY_PRICE_PATH, topdown=False):
        for name in files:
            full_paths.append(os.path.join(root, name))
    return full_paths


def stock_history_save(st_history):
    hist_path =  st_history['hist_path']
    fieldnames =  st_history['fields']
    history_data = st_history['history_data']
    with open(hist_path, 'w', newline='\n') as csvfile:
        d_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        d_writer.writeheader()
        for date_code in sorted(history_data):
            d_writer.writerow(history_data[date_code])


def stock_history_load(stock_symbol):
    """ 
    Load individual stock history files.
    input:
        - hist_path: Stock history path
    output:
        - a stock history (list of dictionaries)
            - fields: in the file
            - history_data: dictionary histories keyed on date code.
            - file_exists: true/false
            - hist_path: The path to the data file
    """
    def convert_date_to_num(date_str):
        month_num_map = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05',
            'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
        d_items = date_str.split('-')
        return int(d_items[2] + month_num_map[d_items[1]] + d_items[0])
    hist_path = define_stock_hist_path(stock_symbol)
    d_reader_fields = []
    stock_historicals = {}
    fDE = os.path.isfile(hist_path)
    if fDE:
        with open(hist_path, 'r', newline='\n') as csvfile:
            d_reader = csv.DictReader(csvfile)
            d_reader_fields = d_reader.fieldnames
            date_code = None
            for h_row in d_reader:
                date_code = convert_date_to_num(h_row['Date'])
                h_row['Open'] = float(h_row['Open'])
                h_row['High'] = float(h_row['High'])
                h_row['Low'] = float(h_row['Low'])
                h_row['Close'] = float(h_row['Close'])
                h_row['Volume'] = int(h_row['Volume'])
                ### this method should weed out any duplicate lines.
                stock_historicals.update({
                    date_code: h_row
                })
            push_date_code_latest(date_code)
    return {
        'hist_path': hist_path,
        'fields': d_reader_fields,
        'history_data': stock_historicals,
        'file_exists': fDE
    }


#####
# other methods
#####


def kill_dict_key(dict_object, dead_key):
    if dead_key in dict_object:
        do_nothing = dict_object.pop(dead_key)
    return dict_object


def push_date_code_latest(date_code_in_question):
    """
    Lastest date code based on stock historicals.
    """
    global date_code_latest
    if date_code_in_question:
        try:
            if date_code_in_question > date_code_latest:
                date_code_latest = date_code_in_question
        except:
            print('Failure in push_date_code_latest')
            print(date_code_latest)
            print(date_code_in_question)
            print(type(date_code_in_question))


def get_date_code_latest():
    global date_code_latest
    return date_code_latest


def define_stock_price_bucket(org_close):
    st_close = float(org_close)
    if st_close < 1:
        return 'penny'
    elif st_close < 5:
        return 'dollar'
    elif st_close < 10:
        return 'deca'
    elif st_close < 50:
        return 'half'
    elif st_close < 100:
        return 'franklin'
    else:
        return 'large'


auto_traider_config_file_load()

