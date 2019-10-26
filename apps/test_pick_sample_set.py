import random
import auto_trader as at

"""
The goal of this script is to take a sample of the production stock data
and save out a sample sub set.
"""

REDUCE_SET_TO = int(at.sys.argv[1])

def create_test_set():
    global REDUCE_SET_TO
    stocks = at.stock_data_file_load()
    if REDUCE_SET_TO > len(stocks):
        REDUCE_SET_TO = len(stocks)
    stocks_test = {}
    sk_keys = random.sample(set(stocks.keys()), REDUCE_SET_TO)
    print('working set', len(sk_keys))
    for st_ct, sk in enumerate(sk_keys):
        stocks_test.update({sk: stocks[sk]})
        if st_ct < 10:
            print(sk, stocks[sk]['companyName'])
    at.test_stock_data_file_save(stocks_test)


def main():
    create_test_set()


if __name__== "__main__":
    main()
