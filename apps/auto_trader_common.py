import os
import json
import csv

### EOD data files
HISTORY_PRICE_PATH = os.path.join('..', 'DATA', 'eod_data_files', 'historicals')
SYMBOL_PATH = os.path.join('..', 'DATA', 'eod_data_files', 'data_files', 'symbols')
STOCK_DAT_FILES = ['AMEX.txt','NYSE.txt','NASDAQ.txt']

### compiled data
HISTORY_PRICE_PROCESSED_LIST_PATH = os.path.join('..', 'DATA', 'historicals', 'processed_dates.dat')
DATA_PATH = os.path.join('..', 'DATA', 'stocks_lists.json')
DATA_PATH_TEST = os.path.join('..', 'DATA', 'stocks_lists_test.json')

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
# file based methods
#####


def define_stock_hist_path(sk):
    return os.path.join('..', 'DATA', 'historicals', sk[:1].lower(), sk.lower() + '.csv')


def write_row_to_file(row_list, header_list, data_file, is_testing=False):
    def make_list_string(my_list):
        new_list = []
        for li in my_list:
            new_list.append(str(li))
        return new_list
    fDE = os.path.isfile(data_file)
    if not fDE:
        if is_testing:
            print('Writing out new stock file: ' + data_file)
        with open(data_file, 'w') as fo:
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


#####
# other methods
#####

def get_highest_historial_price(days, historical_path):
    """
    input:
        - days: number days to dive into the history
        - historical_path: path of history file
    output:
        - highest_price: highest price across selected history
        - last_price_is_highest: was the last highest the highest
        - highest_price_date: what was the hight price
    """
    def convert_date_to_num(date_str):
        month_num_map = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05',
            'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}
        d_items = row['Date'].split('-')
        return d_items[2] + month_num_map[d_items[1]] + d_items[0]
    prices = {}
    highest_price = 0.0
    last_price_is_highest = False
    highest_price_date = ''
    if os.path.isfile(historical_path):
        with open(historical_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_ct, row in enumerate(reader):
                date_code = convert_date_to_num(row['Date'])
                prices.update({date_code: row['Close']})
        for dt_code in sorted(prices.keys())[-1*days:]:
            this_price = float(prices[dt_code])
            is_highest = False
            if highest_price < this_price:
                is_highest = True
                highest_price = this_price
                highest_price_date = dt_code
            # print(dt_code, this_price, is_highest)
            last_price_is_highest = is_highest
    return {
        'highest_price': highest_price,
        'last_price_is_highest': last_price_is_highest,
        'highest_price_date': highest_price_date,
        }


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

