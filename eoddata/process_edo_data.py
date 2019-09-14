import os
import csv
import json

STOCK_DAT_FILES = ['AMEX.txt','NYSE.txt','NASDAQ.txt']
SYMBOL_PATH = os.path.join('data_files', 'symbols')
HISTORY_PRICE_PATH = os.path.join('data_files', 'historicals')
HISTORY_PRICE_PROCESSED_LIST_PATH = os.path.join('..', 'DATA', 'historicals', 'processed_dates.dat')
DATA_PATH = os.path.join('..', 'DATA', 'stocks_lists.json')
MAX_DAYS_TO_PROCESS = 100
TESTING = False

stocks = {}
history_price_processed = set()


def build_stock_histories():
    global stocks
    global history_price_processed
    for f_ct, f_name in enumerate(os.listdir(HISTORY_PRICE_PATH)):
        """ if the max days is reached, then exit the loop """
        if f_ct >= MAX_DAYS_TO_PROCESS:
            print('MAX_DAYS_TO_PROCESS value reached:' + str(MAX_DAYS_TO_PROCESS))
            break
        exchange, date_code = f_name.split('.')[0].split('_')
        hist_file = os.path.join(HISTORY_PRICE_PATH, f_name)
        stocks_found = 0
        if TESTING:
            print('next file: ' + hist_file)
        if f_name not in history_price_processed:
            """ If the downloaded file is in the history processed file, then skip it and delete. """
            history_price_processed.add(f_name)
            with open(hist_file, 'r') as csvfile:
                if TESTING:
                    print('found non dup: ' + hist_file)    
                dict_reader = csv.DictReader(csvfile, delimiter=',')
                for dr_ct, data_row in enumerate(dict_reader):
                    stocks_found += 1
                    sk = data_row['Symbol']
                    sk_hist_path = define_stock_hist_path(sk)
                    make_dir_if_not_exists(sk_hist_path)
                    if not TESTING:
                        write_row_to_file([
                            data_row['Symbol'], data_row['Date'], data_row['Open'], data_row['High'],
                            data_row['Low'], data_row['Close'], data_row['Volume']
                            ], ['Symbol','Date','Open','High','Low','Close','Volume'], 
                            sk_hist_path)
                    # elif not os.path.isfile(sk_hist_path) and dr_ct < 10 and TESTING:
                    #     print([
                    #         data_row['Symbol'], data_row['Date'], data_row['Open'], data_row['High'],
                    #         data_row['Low'], data_row['Close'], data_row['Volume']
                    #         ], ['Symbol','Date','Open','High','Low','Close','Volume'], 
                    #         sk_hist_path, os.path.isfile(sk_hist_path))
                    # elif dr_ct < 10 and TESTING:
                    #     print([
                    #         data_row['Symbol'], data_row['Date'], data_row['Open'], data_row['High'],
                    #         data_row['Low'], data_row['Close'], data_row['Volume']
                    #         ], ['Symbol','Date','Open','High','Low','Close','Volume'], 
                    #         sk_hist_path, os.path.isfile(sk_hist_path), stocks_found)
                    if sk not in stocks:
                        stocks.update({data_row['Symbol']: {
                            'Description': '',
                            'Exchange': exchange,
                            'Historicals': sk_hist_path,
                            'price_bucket': ''
                            }})
        print(hist_file, exchange, date_code, stocks_found)
        if stocks_found > 0:
            if TESTING:
                print('removing file:' + f_name + ' which has ' + str(stocks_found) + ' stocks found.')
            os.remove(hist_file)


def write_row_to_file(row_list, header_list, data_file):
    def make_list_string(my_list):
        new_list = []
        for li in my_list:
            new_list.append(str(li))
        return new_list
    fDE = os.path.isfile(data_file)
    if not fDE:
        if  TESTING:
            print('Writing out new stock file: ' + data_file)
        with open(data_file, 'w') as fo:
            fo.write(','.join(make_list_string(header_list)) + '\n')
    with open(data_file, 'a') as fo:
        fo.write(','.join(make_list_string(row_list)) + '\n')

            
### load stocks into memory
def process_stock_list():
    global stocks
    from_stock_list_ct = 0
    for d_file_ct, d_file in enumerate(STOCK_DAT_FILES):
        d_path = os.path.join(SYMBOL_PATH, d_file)
        with open(d_path, 'r') as csvfile:
            dict_reader = csv.DictReader(csvfile, delimiter='\t')
            for data_row in dict_reader:
                from_stock_list_ct += 1
                sk = data_row['Symbol']
                sk_hist_path = define_stock_hist_path(sk)
                if d_file_ct < 1:
                    make_dir_if_not_exists(sk_hist_path)
                stocks.update({sk: {
                    'Description': data_row['Description'],
                    'Exchange': d_file.replace('.txt', ''),
                    'Historicals_path': sk_hist_path,
                    'price_bucket': ''
                    }})
    print('Updated from stock lists:', from_stock_list_ct)


def define_stock_price_bucket(or_close):
    st_close = float(or_close)
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


def define_stock_hist_path(sk):
    return os.path.join('..', 'DATA', 'historicals', sk[:1].lower(), sk.lower() + '.csv')


def make_dir_if_not_exists(file_path):
    dir_path = os.path.dirname(file_path)
    isD = os.path.isdir(dir_path)
    if not isD:
        os.makedirs(dir_path)
        print('made directory:', dir_path)


def save_history_dates_processed():
    global history_price_processed
    with open(HISTORY_PRICE_PROCESSED_LIST_PATH, 'w') as fo:
        fo.write('\n'.join(history_price_processed))
    print('Processed histories saved:', len(history_price_processed))


def load_history_dates_processed():
    global history_price_processed
    if os.path.isfile(HISTORY_PRICE_PROCESSED_LIST_PATH):
        with open(HISTORY_PRICE_PROCESSED_LIST_PATH, "r") as fi:
            for item in fi:
                history_price_processed.add(item.strip())
    print('Processed histories loaded:', len(history_price_processed))


def save_data_file():
    global stocks
    with open(DATA_PATH, 'w') as fo:
        json.dump(stocks, fo, sort_keys=True, indent=4)
    print('Stocks saved:', len(stocks))


def load_data_file():
    global stocks
    if os.path.isfile(DATA_PATH):
        with open(DATA_PATH, "r") as fi:
            stocks = json.load(fi)
    print('Stocks loaded:', len(stocks))


def main():

    load_data_file()
    load_history_dates_processed()

    process_stock_list()
    build_stock_histories()

    if not TESTING:
        save_data_file()
        save_history_dates_processed()

  
if __name__== "__main__":
    main()
