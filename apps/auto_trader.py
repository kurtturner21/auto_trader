import os
import json
import csv
import sys
import requests
from datetime import datetime


APP_BASE = os.path.join('c:' + os.sep, 'dev', 'auto_trader')
DATA_FILES_BASE = os.path.join('c:' + os.sep, 'auto_trader_data')
APP_CONFIG_DIR = os.path.join('c:' + os.sep, 'dev', 'auto_trader', 'etc')
APP_KILL_FILE = os.path.join('c:' + os.sep, 'dev', 'auto_trader', 'etc', 'delete_me_to_stop_app.kill_file.txt')

### EOD data files
DOWNLOADED_HISTORY_PRICE_PATH = os.path.join(DATA_FILES_BASE, 'eod_data_files', 'downloaded')
SYMBOL_PATH = os.path.join(DATA_FILES_BASE, 'eod_data_files', 'data_files', 'symbols')
STOCK_DAT_FILES = ['AMEX.txt','NYSE.txt','NASDAQ.txt']

### compiled data
HISTORY_PRICE_PROCESSED_LIST_PATH = os.path.join(DATA_FILES_BASE, 'processed_dates.dat')
HISTORY_PRICE_PATH = os.path.join(DATA_FILES_BASE, 'historicals')
COMPANY_INFO_PATH = os.path.join(DATA_FILES_BASE, 'company_info')
DATA_PATH = os.path.join(DATA_FILES_BASE, 'stocks_lists.json')
DATA_PATH_TEST = os.path.join(DATA_FILES_BASE, 'stocks_lists_test.json')

### IEX
IEX_URL_BASE_PROD = 'https://cloud.iexapis.com/stable'      # production
IEX_URL_BASE_TEST = 'https://sandbox.iexapis.com/stable'     # for testing
IEX_TOKEN_PATHS = os.path.join(DATA_FILES_BASE, 'iex', 'iex_tokens.json')
IEX_ACCOUNT_METADATA = os.path.join(DATA_FILES_BASE,'iex', 'account_metadata.json')
IEX_UNKNOWN_SYMBOLS = os.path.join(DATA_FILES_BASE, 'iex', 'unkown_symbols.json')

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


#####
# data objects
#####
def create_stock_lists_stock(sk_symbol):
    return {
        "companyName": "",
        "exchange": "",
        "Historcials_file_exists": "",
        "Historicals_path": define_stock_hist_path(sk_symbol),
        "iex_company_info_path": "",
        "iex_company_info_effect_epoch": "",
        "current_and_usable": "",
        "datecode_count": "",
        "datecode_first": "",
        "datecode_last": "",
        "datecode_last_close": "",
        "price_bucket": "",
        "industry": ""
    }


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
    global idx_unknown_symbols
    api_call = False
    if sk_symbol in idx_unknown_symbols:
        return {'data': {}, 'file_path': '', 'api_call': False, 'unknown_symbol': True}
    key_fact_data_path = define_stock_iex_key_facts(sk_symbol)
    make_dir_if_not_exists(key_fact_data_path)
    if not os.path.isfile(key_fact_data_path):
        api_call = True
        iex_tokens = iex_load_tokens()
        end_point = '/stock/{0}/stats'.format(sk_symbol)
        r_url = IEX_URL_BASE_PROD + end_point + '?token=' + iex_tokens['production_secret']
        r = requests.get(r_url)
        key_facts = {}
        try:
            key_facts = json.loads(r.text)
            key_facts = iex_stock_key_facts_fix(key_facts)
            with open(key_fact_data_path, 'w') as fo:
                fo.write(json.dumps(key_facts, indent=4, sort_keys=True))
        except:
            if 'Unknown symbol' in r.text:
                iex_unknown_symbols_add(sk_symbol)
            print(r.text)
    else:
        with open(key_fact_data_path, "r") as fi:
            key_facts = json.load(fi)
            key_facts = iex_stock_key_facts_fix(key_facts)
    return {
        'data': key_facts,
        'file_path': key_fact_data_path,
        'api_call': api_call,
        'unknown_symbol': False
        }


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


def iex_stock_company_get_info(sk_symbol):
    global idx_unknown_symbols
    api_call = False
    if sk_symbol in idx_unknown_symbols:
        return {'data': {}, 'file_path': '', 'api_call': False, 'unknown_symbol': True}
    company_data_path = define_stock_iex_company_info(sk_symbol)
    ### fixing data
    make_dir_if_not_exists(company_data_path)
    if not os.path.isfile(company_data_path):
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


# def iex_stock_news_get(sk_symbol):
#     ### NOT FINISHED
#     global idx_unknown_symbols
#     api_call = False
#     if sk_symbol in idx_unknown_symbols:
#         return {'data': {}, 'file_path': '', 'api_call': False, 'unknown_symbol': True}
#     news_path = define_stock_iex_news(sk_symbol)
#     make_dir_if_not_exists(news_path)


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
# date time methods
#####


def find_hours_since_epoch(object_data, object_field):
    if object_field not in object_data:
        return -1
    elif object_data[object_field] == '':
        return -1
    elif object_field in object_data:
        epoch_now = float(datetime.now().timestamp())
        try:
            return round(float(epoch_now - float(object_data[object_field]))/60/60, 6)
        except:
            print("FAIL, find_hours_since_epoch: ", object_data, object_field)
            sys.exit(20)
    else:
        return -1


def generate_effective_epoch():
    return datetime.timestamp(datetime.now())


def generate_effective_string():
    return str(datetime.now())


#####
# file based methods
#####


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
    ### dated by sk_year_month.json
    file_name_suffix = datetime.strftime(datetime.now(), '%Y_%m')
    return os.path.join(COMPANY_INFO_PATH, sk[:1].lower(), '_' + sk.lower() + '_iex_key_facts_' + file_name_suffix + '.json')


def define_stock_iex_news(sk):
    return os.path.join(COMPANY_INFO_PATH, sk[:1].lower(), '_' + sk.lower() + '_news.json')


def define_stock_iex_company_info(sk):
    return os.path.join(COMPANY_INFO_PATH, sk[:1].lower(), '_' + sk.lower() + '_iex_compnay_info.json')


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


def stock_history_load(hist_path):
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
    try:
        if date_code_in_question > date_code_latest:
            date_code_latest = date_code_in_question
    except:
        print('Failure in push_date_code_latest')
        print(date_code_latest)
        print(date_code_in_question)
        print(type(date_code_in_question))


# def date_code_latest_save():
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

