import auto_trader as at

def review_history():
    stime = at.datetime.now().timestamp()
    TESTING = at.get_run_in_testing()
    if TESTING:
        stocks = at.test_stock_data_file_load()
    else:
        stocks = at.stock_data_file_load()
    for sk_ct, sk in enumerate(sorted(stocks)):
        # if at.filter_me(stocks[sk]):
        #     continue
        if 'tslx' != sk:
            continue
        at.printing_stock_standard(sk_ct, stocks[sk], 'one')
        at.print_stock_news(sk)
        st_history_data = at.stock_history_load(sk)
        # print(st_history_data.keys())
        at.print_stock_history(sk, days_into_past=10, to_reverse=False)
        at.print_stock_history(sk, days_into_past=10, to_reverse=True)
        print(stocks[sk])



def main():
    review_history()

  
if __name__== "__main__":
    main()