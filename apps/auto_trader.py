import os
import json
import csv
import sys
import requests
from datetime import datetime


APP_BASE = os.path.join('c:' + os.sep, 'dev', 'auto_trader')
DATA_FILES_BASE = os.path.join('c:' + os.sep, 'auto_trader_data')

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


def iex_account_metadata():
    iex_tokens = iex_load_tokens()
    end_point = '/account/metadata'
    r_url = IEX_URL_BASE_PROD + end_point + '?token=' + iex_tokens['production_secret']
    r = requests.get(r_url)
    try:
        account_data = json.loads(r.text)
        with open(IEX_ACCOUNT_METADATA, 'w') as fo:
            fo.write(json.dumps(account_data, indent=4, sort_keys=True))
        print(account_data)
    except:
        print(r.text)


def iex_stock_company_get_info(sk_symbol, contact_iex=True):
    global idx_unknown_symbols
    api_call = False
    if sk_symbol in idx_unknown_symbols:
        return {'data': {}, 'file_path': '', 'api_call': False, 'unknown_symbol': True}
    company_data_path = define_stock_iex_company_info(sk_symbol)
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
            with open(company_data_path, 'w') as fo:
                fo.write(json.dumps(company_data, indent=4, sort_keys=True))
        except:
            if 'Unknown symbol' in r.text:
                iex_unknown_symbols_add(sk_symbol)
            print(r.text)
    else:
        with open(company_data_path, "r") as fi:
            company_data = json.load(fi)
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


#####
# date time methods
#####

def generate_effective_epoch():
    return datetime.timestamp(datetime.now())


def generate_effective_string():
    return str(datetime.now())


#####
# file based methods
#####


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

# def get_highest_historial_price_broken(days, historical_path):
#     """
#     input:
#         - days: number days to dive into the history
#         - historical_path: path of history file
#     output:
#         - highest_price: highest price across selected history
#         - last_price_is_highest: was the last highest the highest
#         - highest_price_date: what was the hight price
#         - last_price: is the last price in the data file
#     """
#     prices = {}
#     highest_price = 0.0
#     last_price_is_highest = False
#     highest_price_date = ''
#     this_price = 0.0
#     if os.path.isfile(historical_path):
#         with open(historical_path) as csvfile:
#             reader = csv.DictReader(csvfile)
#         for dt_code in sorted(prices.keys())[-1*days:]:
#             this_price = float(prices[dt_code])
#             is_highest = False
#             if highest_price < this_price:
#                 is_highest = True
#                 highest_price = this_price
#                 highest_price_date = dt_code
#             # print(dt_code, this_price, is_highest)
#             last_price_is_highest = is_highest
#     return {
#         'highest_price': highest_price,
#         'last_price_is_highest': last_price_is_highest,
#         'highest_price_date': highest_price_date,
#         'last_price': this_price
#         }



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

