import os
import csv
import json
import auto_trader_common as at


def process_new_stock_data():
    MAX_DAYS_TO_PROCESS = 100
    TESTING = False
    stocks = at.stock_data_file_load()
    history_price_processed = at.history_dates_processed_load()
    for f_ct, f_name in enumerate(os.listdir(at.HISTORY_PRICE_PATH)):
        """ if the max days is reached, then exit the loop """
        if f_ct >= MAX_DAYS_TO_PROCESS:
            print('MAX_DAYS_TO_PROCESS value reached:' + str(MAX_DAYS_TO_PROCESS))
            break
        exchange, date_code = f_name.split('.')[0].split('_')
        hist_file = os.path.join(at.HISTORY_PRICE_PATH, f_name)
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
                    sk_hist_path = at.define_stock_hist_path(sk)
                    at.make_dir_if_not_exists(sk_hist_path)
                    if not TESTING:
                        at.write_row_to_file([
                            data_row['Symbol'], data_row['Date'], data_row['Open'], data_row['High'],
                            data_row['Low'], data_row['Close'], data_row['Volume']
                            ], ['Symbol','Date','Open','High','Low','Close','Volume'], 
                            sk_hist_path, TESTING)
                    elif dr_ct < 10 and TESTING:
                        print([
                            data_row['Symbol'], data_row['Date'], data_row['Open'], data_row['High'],
                            data_row['Low'], data_row['Close'], data_row['Volume']
                            ], ['Symbol','Date','Open','High','Low','Close','Volume'], 
                            sk_hist_path, os.path.isfile(sk_hist_path), stocks_found)
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
    if not TESTING:
        at.stock_data_file_save(stocks)
        at.history_dates_processed_save(history_price_processed)


def main():
    process_new_stock_data()


if __name__== "__main__":
    main()
