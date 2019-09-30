import auto_trader as at
import string

TESTING = at.get_run_in_testing()
SLEEP_TIME_OUT_ON_IEX = at.get_sleep_time_out_on_iex()

def process_new_stock_data():
    MAX_DAYS_TO_PROCESS = 30
    history_price_processed = at.history_dates_processed_load()
    for f_ct, f_name in enumerate(at.os.listdir(at.DOWNLOADED_HISTORY_PRICE_PATH)):
        """ if the max days is reached, then exit the loop """
        if TESTING:
            print(f_ct, f_name)
        if f_ct >= MAX_DAYS_TO_PROCESS:
            print('MAX_DAYS_TO_PROCESS value reached:' + str(MAX_DAYS_TO_PROCESS))
            break
        exchange, date_code = f_name.split('.')[0].split('_')
        hist_file = at.os.path.join(at.DOWNLOADED_HISTORY_PRICE_PATH, f_name)
        stocks_found = 0
        if TESTING:
            print('next file: ' + hist_file)
        if f_name not in history_price_processed:
            """ If the downloaded file is in the history processed file, then skip it and delete. """
            history_price_processed.add(f_name)
            with open(hist_file, 'r') as csvfile:
                if TESTING:
                    print('found non dup: ' + hist_file)    
                dict_reader = at.csv.DictReader(csvfile, delimiter=',')
                for data_row in dict_reader:
                    stocks_found += 1
                    sk = data_row['Symbol'].lower()
                    sk_hist_path = at.define_stock_hist_path(sk)
                    at.make_dir_if_not_exists(sk_hist_path)
                    if not TESTING:
                        at.write_row_to_file([
                            sk, data_row['Date'], data_row['Open'], data_row['High'],
                            data_row['Low'], data_row['Close'], data_row['Volume']
                            ], ['Symbol','Date','Open','High','Low','Close','Volume'], 
                            sk_hist_path)
                    if sk not in stocks:
                        stocks.update({sk: {'exchange': exchange}})
        print(hist_file, exchange, date_code, stocks_found)
        if stocks_found > 0:
            if TESTING:
                print('removing file:' + f_name + ' which has ' + str(stocks_found) + ' stocks found.')
            else:
                at.os.remove(hist_file)
        ### check break file not every loop, but every so often
        if at.kill_file_check():
            break
    if not TESTING:
        at.stock_data_file_save(stocks)
        at.history_dates_processed_save(history_price_processed)


def evaluate_duplicates():
    """
    The act of opening the data files with keys and saving them dedups the files. 
    """
    for st_ct, sk in enumerate(sorted(stocks)):
        st_history = at.stock_history_load(sk)
        if st_ct % 1000 == 0: 
            st_history_datecode_count = len(st_history['history_data'].keys())
            stock_status_print_format_str = "{0:<5}{1:<10}{2:<100}day ct:{3:<5}"
            print(stock_status_print_format_str.format(st_ct, sk, st_history_datecode_count))
        at.stock_history_save(st_history)
        ### check break file not every loop, but every so often
        if st_ct % 10 == 0:
            if at.kill_file_check():
                break


def populate_buckets():
    for st_ct, sk in enumerate(sorted(stocks)):
        st_history = at.stock_history_load(sk)
        st_hist_file_exists = st_history['file_exists']
        st_history_datecode_first = ''
        st_history_datecode_last = ''
        st_history_datecode_last_close = ''
        st_history_datecode_count = 0
        p_bucket = ''
        if st_history['history_data']:
            st_history_datecode_first = sorted(st_history['history_data'].keys())[0]
            st_history_datecode_last = sorted(st_history['history_data'].keys())[-1]
            st_history_datecode_last_close = float(st_history['history_data'][st_history_datecode_last]['Close'])
            st_history_datecode_count = len(st_history['history_data'].keys())
            p_bucket = at.define_stock_price_bucket(st_history_datecode_last_close)
        stocks[sk]['price_bucket'] = p_bucket
        stocks[sk].update({'historcials_file_exists':st_hist_file_exists}) 
        stocks[sk].update({'datecode_first':st_history_datecode_first}) 
        stocks[sk].update({'datecode_last':st_history_datecode_last}) 
        stocks[sk].update({'datecode_last_close':st_history_datecode_last_close}) 
        stocks[sk].update({'datecode_count':st_history_datecode_count}) 
        ### check break file not every loop, but every so often
        if st_ct % 10 == 0:
            if at.kill_file_check():
                break

                
def get_iex_comp_info():
    global api_call_count
    HOURS_BETWEEN_IEX_COMP_INFO = at.get_hours_between_iex_comp_info()
    for sk in stocks:
        pull_new_data = True
        if 'iex_company_info_effect_epoch' in stocks[sk]:
            sk_hrs_since_iex_comp_info = at.find_hours_since_epoch(stocks[sk]['iex_company_info_effect_epoch'])
            if sk_hrs_since_iex_comp_info < HOURS_BETWEEN_IEX_COMP_INFO:
                pull_new_data = False
        if pull_new_data:
            # print('diving deep', sk, pull_new_data)
            company_info = at.iex_stock_company_get_info(sk, pull_new_data)
            company_info_data = at.iex_stock_company_fix_info(company_info['data'])
            stocks[sk].update({'employees': company_info_data['employees']})
            stocks[sk].update({'tags': company_info_data['tags']})
            stocks[sk].update({'industry': company_info_data['industry']})
            stocks[sk].update({'sector': company_info_data['sector']})
            stocks[sk].update({'issueType': company_info_data['issueType']})
            stocks[sk].update({'country': company_info_data['country']})
            stocks[sk].update({'iex_unknown_symbol': company_info['unknown_symbol']})
            stocks[sk].update({'iex_company_info_effect_epoch': at.generate_effective_epoch()})
        ### cleaning - Temporary
        if not stocks[sk]['country']:
            stocks[sk]['country'] = ''
        if not stocks[sk]['industry']:
            stocks[sk]['industry'] = ''


def get_iex_key_facts():
    global api_call_count
    for sk_ct, sk in enumerate(sorted(stocks)):
        sk_key_facts = {}
        sk_key_facts = at.iex_stock_get_key_facts(sk)
        if sk_key_facts['api_call']:
            api_call_count += 1
        if api_call_count % SLEEP_TIME_OUT_ON_IEX == 0 and api_call_count > 0:
            print('take time to sleep, api_call_count:' + str(api_call_count))
            at.iex_account_metadata_display()
            at.sleep(5)
        # print(sk, sk_key_facts)
        stocks[sk].update({'iex_key_facts_epoch': sk_key_facts['latest_epoch']})
        keys_to_update = ['peRatio','nextDividendDate','nextEarningsDate','dividendYield',
            'day200MovingAvg','day50MovingAvg','week52high','week52low']
        for ktu in keys_to_update:
            if ktu in sk_key_facts['data']:
                stocks[sk].update({ktu: sk_key_facts['data'][ktu]})
        if sk_ct % 500 == 0:
            print(sk_ct, ' running updates on get_iex_key_facts ', sk)


def check_last_time_ran(module_name):
    to_run = False
    last_time_ran = at.get_last_time_ran()
    last_time_epoch = last_time_ran[module_name]['last_time_epoch']
    hours_between_dedup = last_time_ran[module_name]['hours_between']
    last_dup_in_hours = at.find_hours_since_epoch(last_time_epoch)
    if last_dup_in_hours > hours_between_dedup:
        print('\n{0} {1} hours, running it now.'.format(module_name, last_dup_in_hours))
        last_time_ran[module_name]['last_time_epoch'] = at.generate_effective_epoch()
        at.set_last_time_ran(last_time_ran)
        to_run = True
    else:
        print('\n{0} {1} hours, waiting until next time.'.format(module_name, last_dup_in_hours))
    return to_run


def cleaning_stock_data():
    # ### remove a key
    for sk in sorted(stocks):
        stocks[sk] = at.kill_dict_key(stocks[sk], 'iex_news_epoch_pulled_last')
        stocks[sk].update({'symbol': sk})
    


def get_iex_news():
    global api_call_count
    rounded_api_call_count = 0
    hours_to_collect_news_for_zeros = at.get_hours_to_collect_news_for_zeros()
    print('\nSTARTING to pull NEWS!!!\n')
    for st_ct, sk in enumerate(sorted(stocks)):
        avg_days_per_news = 0
        days_sicne_last_api = 0
        run_api = True
        stocks[sk]['news_existing_ct'] = at.iex_get_exising_news_item_count(sk)    #Only needed once.
        if 'iex_news_epoch' in stocks[sk]:
            days_sicne_last_api = round(at.find_hours_since_epoch(stocks[sk]['iex_news_epoch'])/24, 3)
        else:
            days_sicne_last_api = 10000
        if 'news_oldest_item_epoch' in stocks[sk]:
            if stocks[sk]['news_existing_ct'] > 0:
                days_since_oldest_entry = at.find_hours_since_epoch(stocks[sk]['news_oldest_item_epoch']/1000)/24
                avg_days_per_news = round(days_since_oldest_entry / stocks[sk]['news_existing_ct'], 3)
                run_api = (avg_days_per_news * 2) < days_sicne_last_api or days_sicne_last_api > 15
        ### if nothing and last api was under limit, then don't check. 
        if stocks[sk]['news_existing_ct'] == 0 and days_sicne_last_api < hours_to_collect_news_for_zeros:
            continue
        if run_api:
            news = at.iex_stock_news_get(sk)
            ### just for counts
            if news['api_call']:
                api_call_count += news['news_returned_count']
                rounded_api_call_count += int(float(news['news_returned_count'])/10) * 10
            ### getting avg_days/news
            total_news_ct_after_run = (news['news_existing_ct'] + news['news_new_count'])
            if avg_days_per_news == 0 and total_news_ct_after_run > 0:
                days_since_oldest_entry = at.find_hours_since_epoch(news['news_oldest_item_epoch_in_set']/1000)/24
                avg_days_per_news = round((days_since_oldest_entry /  total_news_ct_after_run), 3)
            print('{0:<8} existing: {1:<10} called: {2:<10} new: {3:<10} avg_days/news: {4:<10}  days_api: {5:<10}  run_api: {6:<10}'.format(
                sk, 
                news['news_existing_ct'],
                news['news_returned_count'],
                news['news_new_count'], 
                avg_days_per_news, 
                days_sicne_last_api,
                str(run_api)
            ))
            stocks[sk].update({'news_returned_count': news['news_returned_count']})
            stocks[sk].update({'news_new_count': news['news_new_count']})
            stocks[sk].update({'news_existing_ct': news['news_existing_ct']})
            stocks[sk].update({'news_oldest_item_epoch': news['news_oldest_item_epoch_in_set']})
            stocks[sk].update({'iex_news_epoch': at.generate_effective_epoch()})
        # else:
        #     print('{0:<8} existing: {1:<10} called: {2:<10} new: {3:<10} avg_days/news: {4:<10}  days_api: {5:<10}  run_api: {6:<10}'.format(
        #         sk, stocks[sk]['news_existing_ct'], 0, 0, avg_days_per_news, days_sicne_last_api, str(run_api)))
        ### check break file not every loop, but every so often
        # if rounded_api_call_count % SLEEP_TIME_OUT_ON_IEX == 0 and api_call_count > 0:
        #     print('take time to sleep, api_call_count:' + str(api_call_count))
        #     at.iex_account_metadata_display()
        #     at.sleep(5)
        if st_ct % 10 == 0:
            if at.kill_file_check():
                break
    print('\n')


def process_new_retings_data():
    r_login_info = at.r_login()
    print('\nSTARTING to pull RATINGS!!!\n')
    update_sks = 0
    for sk_ct, sk in enumerate(sorted(stocks)):
        if 'rh_error_code' in stocks[sk]:
            if stocks[sk]['rh_error_code'] > 0:
                continue
        diff_in_hours = 10000
        if 'rh_api_epoch' in stocks[sk]:
            diff_in_hours = (at.datetime.now().timestamp() - stocks[sk]['rh_api_epoch']) / 60 / 60
        if diff_in_hours > 72:
            update_sks += 1
            rh_ratings = at.r_get_ratings(sk)
            stocks[sk].update({'rh_hold': rh_ratings['hold']})
            stocks[sk].update({'rh_buy': rh_ratings['buy']})
            stocks[sk].update({'rh_sell': rh_ratings['sell']})
            stocks[sk].update({'rh_api_epoch': rh_ratings['last_rh_api_epoch']})
            stocks[sk].update({'rh_error_code': rh_ratings['error_code']})
            str_fmt = '{0:>10} {1:>10} sell:{2:<5} hold:{3:<5} buy:{4:<5}  days since last: {5:<10}  e_code: {6}'
            print(str_fmt.format(sk_ct, sk, rh_ratings['sell'], rh_ratings['hold'], rh_ratings['buy'], 
                diff_in_hours, rh_ratings['error_code']))
    print('update_sks: ' + str(update_sks))
    at.r_logout()


def main():
    global stocks
    global api_call_count
    at.iex_account_metadata_display()
    api_call_count = 0
    if TESTING:
        stocks = at.test_stock_data_file_load()
    else:
        stocks = at.stock_data_file_load()
    overall_stime = at.datetime.now().timestamp()
    at.iex_unknown_symbols_load()
    at.kill_file_touch()
    print('-----------------app started--------------------')
    # cleaning_stock_data()

    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('process_new_stock_data'):
        process_new_stock_data()
        if TESTING:
            at.test_stock_data_file_save(stocks)
        else:
            at.stock_data_file_save(stocks)
    at.print_process_module_status('process_new_stock_data', this_stime, overall_stime)
    
    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('evaluate_duplicates'):
        evaluate_duplicates()
        if TESTING:
            at.test_stock_data_file_save(stocks)
        else:
            at.stock_data_file_save(stocks)
    at.print_process_module_status('evaluate_duplicates', this_stime, overall_stime)

    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('populate_buckets'):
        populate_buckets()
        if TESTING:
            at.test_stock_data_file_save(stocks)
        else:
            at.stock_data_file_save(stocks)
    at.print_process_module_status('populate_buckets', this_stime, overall_stime)

    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('get_iex_comp_info'):
        get_iex_comp_info()
        if TESTING:
            at.test_stock_data_file_save(stocks)
        else:
            at.stock_data_file_save(stocks)
    at.print_process_module_status('get_iex_comp_info', this_stime, overall_stime)


    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('get_iex_key_facts'):
        get_iex_key_facts()
        if TESTING:
            at.test_stock_data_file_save(stocks)
        else:
            at.stock_data_file_save(stocks)
    at.print_process_module_status('get_iex_key_facts', this_stime, overall_stime)
    get_iex_key_facts()

    process_new_retings_data()
    get_iex_news()


    ### build indexes
    ### score news
    if TESTING:
        at.test_stock_data_file_save(stocks)
    else:
        at.stock_data_file_save(stocks)
    at.iex_account_metadata_display()
    print('IEX api_call_count: ' + str(api_call_count))
    print('-----------------all done with data--------------------')


if __name__== "__main__":
    main()
