import auto_trader as at


def news_reader():
    stime = at.datetime.now().timestamp()
    r_login_info = at.r_login()
    # print(r_login_info)
    TESTING = at.get_run_in_testing()
    if TESTING:
        stocks = at.test_stock_data_file_load()
    else:
        stocks = at.stock_data_file_load()
    found_by_filter_ct = 0
    for sk_ct, sk in enumerate(sorted(stocks)):
        sk_last_close = stocks[sk]['datecode_last_close']
        sk_history_count = stocks[sk]['datecode_count']
        sk_price_bucket = stocks[sk]['price_bucket']
        sk_name = stocks[sk]['companyName']
        sk_news_existing_ct = stocks[sk]['news_existing_ct']
        if sk_news_existing_ct == 0: 
            continue
        if at.filter_me(stocks[sk]):
            continue
        # if sk != 'crc':
        #     continue
        found_by_filter_ct += 1
        rh_ratings = at.r_get_ratings(sk)
        sk_rate_sell_ct = rh_ratings['sell']
        sk_rate_buy_ct = rh_ratings['buy']
        sk_rate_hold_ct = rh_ratings['hold']
        str_fmt = '{0:>10} {1:<10}{2:<50}{3:<5}{4:<10}{5:<5}{6:<10} sell:{7:<5} hold:{8:<5} buy:{9:<5}'
        print(str_fmt.format(sk_ct, sk, sk_name[:46], sk_news_existing_ct, sk_last_close, 
            sk_history_count, sk_price_bucket, sk_rate_sell_ct, sk_rate_hold_ct, sk_rate_buy_ct))
    print('\nfound_by_filter_ct: ' + str(found_by_filter_ct))
    print('Time to process, ', round(at.datetime.now().timestamp() - stime, 2))

def main():
    at.kill_file_touch()
    news_reader()
    at.r_logout()

  
if __name__== "__main__":
    main()
