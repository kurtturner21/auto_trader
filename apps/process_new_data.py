import auto_trader as at
import string
import pandas_datareader.data as web
from datetime import timedelta  

TESTING = at.get_run_in_testing()
SLEEP_TIME_OUT_ON_IEX = at.get_sleep_time_out_on_iex()

def get_cik_with_last10k():
    print('\nSTARTING to get_cik_with_last10k!!!')
    LAST10K_API_COUNT_MAX = at.get_last10k_api_count_max()
    last10k_api_count_current = at.get_last10k_api_count_current()
    last10k_api_count_month = at.get_last10k_api_count_month()
    this_month = int(at.datetime.strftime(at.datetime.now(), '%Y%U')) ### YEAR + WEEKNUM
    if this_month > last10k_api_count_month:
        print('Resetting last10k_api_count_month to: ' + str(this_month))
        last10k_api_count_current = 0
        at.set_last10k_api_count_month(this_month)
    found_cik_ct = 0
    api_call = 0
    for sk_ct, sk in enumerate(sorted(stocks)):
        if 'cik' in stocks[sk]:
            continue
        if api_call > 100:
            break
        if at.kill_file_check():
            break
        at.sleep(12)
        cik = ''
        if last10k_api_count_current <= LAST10K_API_COUNT_MAX:
            last10k_api_count_current += 1
            api_call += 1
            cik_data = at.last10k_cik(sk)
            at.set_last10k_api_count_current(last10k_api_count_current)
            if cik_data == 0:
                stocks[sk].update({ 'cik': cik_data })
            elif 'data' in cik_data:
                found_cik_ct += 1
                cik = cik_data['data']['attributes']['result'][0]
                stocks[sk].update({ 'cik': cik })
            else: 
                print('FAIL on stock ' +sk + ' with data:' + str(cik_data))
        print(sk_ct, sk, cik, api_call)
    print('found_cik_ct: ' + str(found_cik_ct))
    print('last10k_api_count_current: ' + str(last10k_api_count_current))


def get_iex_new_symbols():
    print('\nSTARTING to get_iex_new_symbols!!!')
    iex_symbols = at.iex_symbols()
    new_stocks_found = 0
    for sk_ct, sk_iex_data in enumerate(iex_symbols):
        sk = sk_iex_data['symbol'].lower()
        last_letter = sk[-1]
        if last_letter in ('+', '=', '-', '*', '#', '^'):
            continue
        if sk not in stocks:
            new_stocks_found += 1
            stocks.update({sk: at.create_stock_lists_stock(sk)})
            stocks[sk].update({ 'companyName': sk_iex_data['name'] })
            stocks[sk].update({ 'issueType': sk_iex_data['type'] })
            stocks[sk].update({ 'country': sk_iex_data['region'] })
            print('FOUND NEW SYMBOL: ' + sk + '   ' + sk_iex_data['name'])
    print('new_stocks_found: ' + str(new_stocks_found))


def process_stock_histories():
    print('\nSTARTING to process_stock_histories!!!')
    downloaded_history_count = 0
    new_history_count_oa = 0
    sleep_batch_count = 0
    passed_on_pull_epoch = 0
    passed_on_last_date = 0
    passed_on_no_new_data = 0
    HOURS_BETWEEN_HISTORY_CLOSING_DATES = at.get_hours_between_history_close_dates()
    for sk_ct, sk in enumerate(sorted(stocks)):
        if sk_ct % 500 == 0 and sk_ct > 0:
            print('process_new_stock_data: {0:<6}  downloaded_history_count: {1}  new_history_count_oa: {2}'.format(str(sk_ct),  str(downloaded_history_count), new_history_count_oa))
            if at.kill_file_check():
                break
        if sleep_batch_count > 1000:
            print('process_new_stock_data: sleep batch hit!!! ' + str(sleep_batch_count))
            sleep_batch_count = 0
            at.sleep(5)
        # if sk_ct > 10:           #### testing
        #     break
        sk_file = at.define_stock_hist_path(sk)
        sk_file_de = at.os.path.isfile(sk_file)
        df_existing = at.create_empty_stock_history()
        hours_since_last_download = 10000
        if 'h_pull_epoch' in stocks[sk]:
            hours_since_last_download = at.find_hours_since_epoch(stocks[sk]['h_pull_epoch'])
        hours_since_close_date = 10000
        if 'h_close_date' in stocks[sk]:
            hours_since_close_date = at.find_hours_since_epoch(stocks[sk]['h_close_date'])
        if hours_since_last_download < 24:
            # print(sk_ct, sk,'pass on 24 hour rule')       #### testing
            passed_on_pull_epoch += 1
            continue
        ### if data_not_needed_now is true and less than between hours, then process
        data_not_needed_now = at.filter_for_pulling_stock_histories(stocks[sk])
        if hours_since_close_date < HOURS_BETWEEN_HISTORY_CLOSING_DATES and data_not_needed_now:
            # print(sk_ct, sk,'pass b/c is not critical')       #### testing
            passed_on_last_date += 1
            continue
        ### open existing
        if sk_file_de:
            df_existing = at.pd.read_csv(sk_file, parse_dates=True, index_col=0)
        history_count_before = df_existing['Open'].count()
        ### set range
        start = at.datetime(2000,1,1)
        if df_existing['Open'].count() > 0:
            start = df_existing.index[-1] + timedelta(days=1) 
        end = at.datetime.today()
        ### download or create new file
        try:
            df_downloaded = web.DataReader(sk.upper(), 'yahoo', start, end)
        except:
            df_downloaded = at.create_empty_stock_history()
        stocks[sk].update({ 'h_pull_epoch': at.generate_effective_epoch() })
        ### combine data
        for r_index, price_row in df_downloaded.iterrows():
            df_existing.loc[r_index] = price_row
        ### getting counts
        history_count = df_existing['Open'].count()
        downloaded_history_count += int(df_downloaded['Open'].count())
        sleep_batch_count += int(df_downloaded['Open'].count())
        new_hisotry_count = history_count - history_count_before
        new_history_count_oa += new_hisotry_count
        if new_hisotry_count == 0:
            passed_on_no_new_data += 1
            continue        ### if no new records, then move on. 
        # print(sk_ct, sk, sk_file_de, hours_since_last_download, hours_since_close_date, new_hisotry_count)       #### testing
        # continue                ### testing
        stocks[sk].update({ 'h_count': int(history_count) })
        ### normalize it
        df_existing['5ma'] =  round(df_existing['Adj Close'].rolling(window=5, min_periods=0).mean(),3)
        df_existing['10ma'] =  round(df_existing['Adj Close'].rolling(window=10, min_periods=0).mean(),3)
        df_existing['30ma'] =  round(df_existing['Adj Close'].rolling(window=30, min_periods=0).mean(),3)
        df_existing['100ma'] =  round(df_existing['Adj Close'].rolling(window=100, min_periods=0).mean(),3)
        df_existing['200ma'] =  round(df_existing['Adj Close'].rolling(window=200, min_periods=0).mean(),3)
        df_existing = df_existing.round({'Open': 3, 'High': 3, 'Low': 3, 'Adj Close': 3, 'Close': 3})
        ### update stock data
        if df_existing['Open'].count() > 0:
            sk_his_close = df_existing.loc[df_existing.index[-1]]['Close']
            stocks[sk].update({ 'h_source': 'yahoo' })
            stocks[sk].update({ 'price_bucket': at.define_stock_price_bucket(sk_his_close) })
            stocks[sk].update({ 'h_30ma': df_existing.loc[df_existing.index[-1]]['30ma'] })
            stocks[sk].update({ 'h_100ma': df_existing.loc[df_existing.index[-1]]['100ma'] })
            stocks[sk].update({ 'h_200ma': df_existing.loc[df_existing.index[-1]]['200ma'] })
            stocks[sk].update({ 'h_close': float(sk_his_close) })
            stocks[sk].update({ 'h_close_date': at.human_to_epoch(str(df_existing.index[-1])) })
        else:
            if 'h_source' not in stocks[sk]:
                stocks[sk].update({ 'h_source': '' })
                stocks[sk].update({ 'price_bucket': '' })
                stocks[sk].update({ 'h_30ma': 0 })
                stocks[sk].update({ 'h_100ma': 0 })
                stocks[sk].update({ 'h_200ma': 0 })
                stocks[sk].update({ 'h_close': 0.0 })
                stocks[sk].update({ 'h_close_date': 0 })
        df_existing.sort_index(inplace=True)
        ### save to file
        df_existing.to_csv(sk_file)
        ### counting metrixes
        ### for TESTING  history_count_before
        # print(sk_ct, sk, str(df_existing.index[-1])) 
        # print(sk_ct, sk, at.human_to_epoch(str(df_existing.index[-1])))
        # print(sk_ct, sk, at.epoch_to_human(at.human_to_epoch(str(df_existing.index[-1]))))
        # print(sk_ct, sk, sk_file_de, new_hisotry_count, str(df_existing.index[-1])) 
    print('process_new_stock_data: {0:<6}  downloaded_history_count: {1}  new_history_count_oa: {2}'.format(str(sk_ct),  str(downloaded_history_count), new_history_count_oa))
    print('passed_on_pull_epoch: ' + str(passed_on_pull_epoch))
    print('passed_on_last_date: ' + str(passed_on_last_date))
    print('passed_on_no_new_data: ' + str(passed_on_no_new_data))
    print('downloaded_history_count: ' + str(downloaded_history_count))
    print('overall new histories added: ' + str(new_history_count_oa))
    
                
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
            'week52high','week52low']
        for ktu in keys_to_update:
            if ktu in sk_key_facts['data']:
                stocks[sk].update({ktu: sk_key_facts['data'][ktu]})
        if sk_ct % 500 == 0:
            print(sk_ct, ' running updates on get_iex_key_facts ', sk)
            if at.kill_file_check():
                break


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
        # stocks[sk] = at.kill_dict_key(stocks[sk], '100ma')
        # stocks[sk] = at.kill_dict_key(stocks[sk], '200ma')
        # stocks[sk] = at.kill_dict_key(stocks[sk], '30ma')
        stocks[sk].update({'symbol': sk})
        if 'tags' not in stocks[sk]:
            stocks[sk].update({'tags': []})
        if 'sector' not in stocks[sk]:
            stocks[sk].update({'sector': ''})
        if stocks[sk]['sector'] is None:
            stocks[sk]['sector'] = ''
        if 'country' not in stocks[sk]:
            stocks[sk].update({'country': ''})
        if stocks[sk]['country'] is None:
            stocks[sk]['country'] = 0
        if 'issueType' not in stocks[sk]:
            stocks[sk].update({'issueType': ''})
        if stocks[sk]['issueType'] is None:
            stocks[sk]['issueType'] = ''
        if 'companyName' not in stocks[sk]:
            stocks[sk].update({'companyName': ''})
        if stocks[sk]['companyName'] is None:
            stocks[sk]['companyName'] = ""
        if 'exchange' not in stocks[sk]:
            stocks[sk].update({'exchange': ''})
        if stocks[sk]['exchange'] is None:
            stocks[sk]['exchange'] = ""
        if 'industry' not in stocks[sk]:
            stocks[sk].update({'industry': ''})
        if stocks[sk]['industry'] is None:
            stocks[sk]['industry'] = ""
        if 'employees' not in stocks[sk]:
            stocks[sk].update({'employees': 0})
        if stocks[sk]['employees'] is None:
            stocks[sk]['employees'] = 0

    


def get_iex_news():
    global api_call_count
    rounded_api_call_count = 0
    hours_to_collect_news_for_zeros = at.get_hours_to_collect_news_for_zeros()
    print('\nSTARTING to pull NEWS!!!\n')
    for sk_ct, sk in enumerate(sorted(stocks)):
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
                run_api = (avg_days_per_news * 10) < days_sicne_last_api and days_sicne_last_api > 2
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
        if sk_ct % 10 == 0:
            if at.kill_file_check():
                break
    print('\n')


def process_new_ratings_data():
    r_login_info = at.r_login()
    print('\nSTARTING to pull RATINGS!!!\n')
    update_sks = 0
    for sk_ct, sk in enumerate(sorted(stocks)):
        if 'rh_error_code' in stocks[sk]:
            if stocks[sk]['rh_error_code'] > 0:
                continue
        diff_in_hours = 10000
        if 'rh_api_epoch' in stocks[sk]:
            diff_in_hours = round((at.datetime.now().timestamp() - stocks[sk]['rh_api_epoch']) / 60 / 60, 2)
        if diff_in_hours > 12:
            update_sks += 1
            rh_ratings = at.r_get_ratings(sk)
            stocks[sk].update({'rh_hold': rh_ratings['hold']})
            stocks[sk].update({'rh_buy': rh_ratings['buy']})
            stocks[sk].update({'rh_sell': rh_ratings['sell']})
            stocks[sk].update({'rh_api_epoch': rh_ratings['last_rh_api_epoch']})
            stocks[sk].update({'rh_error_code': rh_ratings['error_code']})
            str_fmt = '{0:>10} {1:>10} sell:{2:<5} hold:{3:<5} buy:{4:<5}  hours since last: {5:<10}  e_code: {6}'
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
    cleaning_stock_data()

    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('get_iex_new_symbols'):
        get_iex_new_symbols()
    at.print_process_module_status('get_iex_new_symbols', this_stime, overall_stime)

    this_stime = at.datetime.now().timestamp()
    # if check_last_time_ran('process_new_ratings_data'):
    process_new_ratings_data()
    at.print_process_module_status('process_new_ratings_data', this_stime, overall_stime)

    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('process_stock_histories'):
        process_stock_histories()
    at.print_process_module_status('process_stock_histories', this_stime, overall_stime)

    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('get_iex_comp_info'):
        get_iex_comp_info()
    at.print_process_module_status('get_iex_comp_info', this_stime, overall_stime)


    this_stime = at.datetime.now().timestamp()
    if check_last_time_ran('get_iex_key_facts'):
        get_iex_key_facts()
    at.print_process_module_status('get_iex_key_facts', this_stime, overall_stime)
    
    get_iex_key_facts()
    get_iex_news()


    # get_cik_with_last10k()    CONNECTION ERRORS

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
