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

APP_BASE = os.path.join('c:' + os.sep, 'dev', 'auto_trader')
DATA_FILES_BASE = os.path.join('c:' + os.sep, 'auto_trader_data')
APP_CONFIG_DIR = os.path.join('c:' + os.sep, 'dev', 'auto_trader', 'etc')
APP_KILL_FILE = os.path.join('c:' + os.sep, 'dev', 'auto_trader', 'etc', 'delete_me_to_stop_app.kill_file.txt')

### EOD data files
DOWNLOADED_HISTORY_PRICE_PATH = os.path.join(DATA_FILES_BASE, 'eod_data_files', 'downloaded')
SYMBOL_PATH = os.path.join(DATA_FILES_BASE, 'eod_data_files', 'data_files', 'symbols')
STOCK_DAT_FILES = ['AMEX.txt','NYSE.txt','NASDAQ.txt']

### compiled data
HISTORY_PRICE_PROCESSED_LIST_PATH = os.path.join(DATA_FILES_BASE, 'etc', 'processed_dates.dat')
HISTORY_PRICE_PATH = os.path.join(DATA_FILES_BASE, 'company_info')
COMPANY_INFO_PATH = os.path.join(DATA_FILES_BASE, 'company_info')
DATA_PATH = os.path.join(DATA_FILES_BASE, 'stocks_lists.json')
DATA_PATH_TEST = os.path.join(DATA_FILES_BASE, 'stocks_lists_test.json')
AUTO_TRADER_CONFIG_PATH = os.path.join(DATA_FILES_BASE, 'etc', 'auto_trader_config.json')

### Robin hood
ROBIN_HOOD_CONFIG_PATH = os.path.join(DATA_FILES_BASE, 'etc', 'robin_hood_creds.json')

### Last10K
LAST10K_CONFIG_PATH = os.path.join(DATA_FILES_BASE, 'etc', 'last10k_keys.json')

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
        DESIRED_COUNTRIES_LIMIT = False
        DESIRED_COUNTRIES = ['US', 'AU', '', None]
        DESIRED_STOCK_ISSUE_TYPE_LIMIT = True
        DESIRED_STOCK_ISSUE_TYPE = ['ps','cs', 'ad', 'si']
        DESIRED_PRICE_BUCKET_LIMIT = False
        DESIRED_PRICE_BUCKET = ['deca', 'dollar','penny', 'half']
        NON_DESIRED_INDUSTRY_LIMIT = False
        NON_DESIRED_INDUSTRY = ['Precious Metals', 'Steel', 'Aluminum', 'Coal']
        MIN_HISTORY_LIMIT = True
        MIN_HISTORY = 200
        DIVIDEND_MIN_LIMIT = True
        DIVIDEND_MIN = .001
        PE_LIMIT = False
        PE_MAX = 40
        PE_MIN = -5
        NEWS_LIMIT = False
        NEWS_MIN = 20
        RH_RATING_LIMIT = True
        RH_RATING_MIN = .95
        rh_rate_score = calculate_rating_score(stock_record)
        filter_me = False
        if stock_record['iex_unknown_symbol']:
            filter_me = True
        if stock_record['country'] not in DESIRED_COUNTRIES and DESIRED_COUNTRIES_LIMIT:
            filter_me = True
        if stock_record['issueType'] not in DESIRED_STOCK_ISSUE_TYPE and DESIRED_STOCK_ISSUE_TYPE_LIMIT:
            filter_me = True
        if stock_record['price_bucket'] not in DESIRED_PRICE_BUCKET and DESIRED_PRICE_BUCKET_LIMIT:
            filter_me = True
        if stock_record['datecode_count'] < MIN_HISTORY and MIN_HISTORY_LIMIT:
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
        print('FAIL: this stock failed the filtering process: ' + stock_record['symbol'])
        sys.exit(20)


#####
# print constructors
#####
def printing_stock_standard(loop_num, stock_record, print_standard='one'):
    rh_rate_score = calculate_rating_score(stock_record)
    if print_standard == 'one':
        stock_row_print_format = '{0:<6}{1:<10}{2:<10}{3:<10}{4:<30}{5:<10}{6:<30}{7:<25}{8:<5}{9:<5}{10:<8}{11:<10} news:{12:<10} rating:{13:<3}'
        print_str = stock_row_print_format.format(loop_num, stock_record['symbol'], stock_record['datecode_last_close'], stock_record['datecode_count'], 
            stock_record['companyName'][:28].encode("ascii", 'ignore').decode("ascii"), stock_record['employees'], stock_record['industry'][:28], 
            stock_record['sector'][:23], stock_record['issueType'], 
            stock_record['country'], stock_record['peRatio'], stock_record['dividendYield'], stock_record['news_existing_ct'],
            rh_rate_score
            )
        print(print_str)
    elif print_standard == 'two':
        stock_row_print_format = '{0:<6}{1[symbol]:<5}{1[issueType]:<8}{1[country]:<10}{1[peRatio]:<10}{1[dividendYield]:<10} rating:{2:<3}'
        print_str = stock_row_print_format.format(loop_num, stock_record, rh_rate_score)
        return print_str
        print(print_str)


def calculate_rating_score(stock_record):
    rh_rate_score_divisor = (stock_record['rh_buy'] + stock_record['rh_hold'] + stock_record['rh_sell'])
    if rh_rate_score_divisor > 0:
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
# stock history functions
#####

def get_sh_52_week_numbers(stock_history):
    # one year of seconds 31536000
    one_year_epoch = generate_effective_epoch() - 31471200
    one_year_datecode = int(time.strftime('%Y%m%d',  gmtime(one_year_epoch)))
    high_52 = 0
    low_52 = 0
    for dt_code in sorted(stock_history, reverse=True):
        if dt_code >= one_year_datecode:
            cur_dt_high = stock_history[dt_code]['High']
            cur_dt_low = stock_history[dt_code]['Low']
            cur_dt_close = stock_history[dt_code]['Close']
            if cur_dt_high > high_52:
                high_52 = cur_dt_high
                print(dt_code, high_52, low_52)
            if cur_dt_low < low_52 or low_52 == 0:
                low_52 = cur_dt_low
                print(dt_code, high_52, low_52)


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


def epoch_to_human(epoch_time):
    epoch_time_float = float(epoch_time)
    if len(str(int(epoch_time_float))) == 10:
        return time.strftime('%m/%d/%Y %H:%M:%S',  gmtime(epoch_time_float))
    else:
        return time.strftime('%m/%d/%Y %H:%M:%S',  gmtime(epoch_time_float/1000.))


#####
# data objects
#####
def create_stock_lists_stock(sk_symbol):
    return {
        "companyName": "",
        "exchange": "",
        "historcials_file_exists": "",
        "iex_company_info_path": "",
        "iex_company_info_effect_epoch": 0,
        "iex_news_epoch": 0,
        "current_and_usable": "",
        "datecode_count": "",
        "datecode_first": "",
        "datecode_last": "",
        "datecode_last_close": "",
        "price_bucket": "",
        "industry": ""
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


#####
# LAST10k functions
#####



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


def last10k_config_file_save():
    global last10k_config
    with open(LAST10K_CONFIG_PATH, 'w') as fo:
        json.dump(rb_config, fo, sort_keys=True, indent=4)


def last10k_config_file_load():
    global last10k_config
    if os.path.isfile(LAST10K_CONFIG_PATH):
        with open(LAST10K_CONFIG_PATH, "r") as fi:
            last10k_config = json.load(fi)


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


# def define_stock_lask10k_


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

def get_stock_symbol_from_path(st_path):
    return os.path.basename(st_path)[1:].split('.')[0]


def write_row_to_file(row_list, header_list, data_file):
    def make_list_string(my_list):
        new_list = []
        for li in my_list:
            new_list.append(str(li))
        return new_list
    fDE = os.path.isfile(data_file)
    if not fDE:
        print('Writing out new stock file: ' + data_file)
        with open(data_file, 'w+') as fo:
            fo.write(','.join(make_list_string(header_list)) + '\n')
    with open(data_file, 'a') as fo:
        fo.write(','.join(make_list_string(row_list)) + '\n')


def make_dir_if_not_exists(file_path):
    dir_path = os.path.dirname(file_path)
    isD = os.path.isdir(dir_path)
    if not isD:
        os.makedirs(dir_path)
        print('made directory:', dir_path)


def history_dates_processed_save(history_price_processed):
    with open(HISTORY_PRICE_PROCESSED_LIST_PATH, 'w') as fo:
        fo.write('\n'.join(history_price_processed))
    print('Processed histories saved:', len(history_price_processed))


def history_dates_processed_load():
    history_price_processed = set()
    if os.path.isfile(HISTORY_PRICE_PROCESSED_LIST_PATH):
        with open(HISTORY_PRICE_PROCESSED_LIST_PATH, "r") as fi:
            for item in fi:
                history_price_processed.add(item.strip())
    print('Processed histories loaded:', len(history_price_processed))
    return history_price_processed


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
