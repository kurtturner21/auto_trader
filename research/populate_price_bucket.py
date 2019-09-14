import os
import csv
import json


DATA_PATH_TEST = os.path.join('..', 'DATA', 'stocks_lists_test.json')
stocks_test = {}


def populate_price_bucket():
    global stocks_test
    for st_ct, sk in enumerate(sorted(stocks_test)):
        highest_price_100d = get_highest_historial_price(100, stocks_test[sk]['Historicals_path'])['highest_price']
        highest_price_200d = get_highest_historial_price(200, stocks_test[sk]['Historicals_path'])['highest_price']
        print(sk, stocks_test[sk]['Description'], highest_price_100d, highest_price_200d)


def get_highest_historial_price(days, historical_path):
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



"""Symbol,Date,Open,High,Low,Close,Volume
E,01-Jan-2014,48.49,48.49,48.49,48.49,0
E,02-Jan-2014,47.72,47.72,47.23,47.32,232600
E,03-Jan-2014,47.64,47.91,47.47,47.74,251100
E,06-Jan-2014,48.05,48.35,47.92,48.1,442800
E,07-Jan-2014,47.92,48.3,47.76,48.3,220600
E,08-Jan-2014,47.74,47.9,47,47,327600
E,09-Jan-2014,47.55,47.59,46.91,46.99,123700"""



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


def save_data_test_file():
    global stocks_test
    with open(DATA_PATH_TEST, 'w') as fo:
        json.dump(stocks_test, fo, sort_keys=True, indent=4)
    print('TEST Stocks saved:', len(stocks_test))


def load_data_test_file():
    global stocks_test
    if os.path.isfile(DATA_PATH_TEST):
        with open(DATA_PATH_TEST, "r") as fi:
            stocks_test = json.load(fi)
    print('TEST Stocks loaded:', len(stocks_test))


def main():
    load_data_test_file()
    populate_price_bucket()
    save_data_test_file()

  
if __name__== "__main__":
    main()
