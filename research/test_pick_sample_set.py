import os
import csv
import json
import random

DATA_PATH = os.path.join('..', 'DATA', 'stocks_lists.json')
DATA_PATH_TEST = os.path.join('..', 'DATA', 'stocks_lists_test.json')
REDUCE_SET = True
REDUCE_SET_TO = 10
stocks = {}
stocks_test = {}


def list_records():
    global stocks
    global stocks_test
    if REDUCE_SET:
        sk_keys = random.sample(set(stocks.keys()), REDUCE_SET_TO)
    print('working set', len(sk_keys))
    for st_ct, sk in enumerate(sk_keys):
        stocks_test.update({sk: stocks[sk]})
        if st_ct < 10:
            print(sk, stocks[sk]['Description'])


def make_dir_if_not_exists(file_path):
    dir_path = os.path.dirname(file_path)
    isD = os.path.isdir(dir_path)
    if not isD:
        os.makedirs(dir_path)
        print('made directory:', dir_path)


def save_data_test_file():
    global stocks_test
    with open(DATA_PATH_TEST, 'w') as fo:
        json.dump(stocks_test, fo, sort_keys=True, indent=4)
    print('TEST Stocks saved:', len(stocks_test))


def load_data_file():
    global stocks
    if os.path.isfile(DATA_PATH):
        with open(DATA_PATH, "r") as fi:
            stocks = json.load(fi)
    print('Stocks loaded:', len(stocks))


def main():
    load_data_file()
    list_records()
    save_data_test_file()

  
if __name__== "__main__":
    main()
