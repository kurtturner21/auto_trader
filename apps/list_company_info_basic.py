import auto_trader as at

def list_all_company_info_basic():
    stime = at.datetime.now().timestamp()
    TESTING = False
    if TESTING:
        stocks = at.test_stock_data_file_load()
    else:
        stocks = at.stock_data_file_load()
    ### for counting
    country_ct = {}
    issueType_ct = {}
    sector_ct = {}
    tags_ct = {}
    price_bucket_ct = {}
    found_by_filter_ct = 0
    ### limit and filters
    OVERALL_LIMIT = 200000         ### used for testing, if production set to over 10000
    DISPLAY_LIMIT = 20000
    DISPLAY_EVERY_NTH = 10
    DESIRED_COUNTRIES_LIMIT = False
    DESIRED_COUNTRIES = ['US', 'AU', '', None]
    DESIRED_STOCK_ISSUE_TYPE_LIMIT = False
    DESIRED_STOCK_ISSUE_TYPE = ['ps','cs', 'ad', 'si']
    DESIRED_PRICE_BUCKET_LIMIT = False
    DESIRED_PRICE_BUCKET = ['deca', 'dollar','penny', 'half']
    NON_DESIRED_INDUSTRY_LIMIT = False
    NON_DESIRED_INDUSTRY = ['Precious Metals', 'Steel', 'Aluminum', 'Coal']
    MIN_HISTORY_LIMIT = False
    MIN_HISTORY = 200
    DIVIDEND_MIN_LIMIT = False
    DIVIDEND_MIN = .001
    PE_LIMIT = False
    PE_MAX = 100
    ### starting to loop over stocks 
    for sk_ct, sk in enumerate(sorted(stocks)):
        try:
            ### extracting from stocks 
            sk_last_close = stocks[sk]['datecode_last_close']
            sk_history_count = stocks[sk]['datecode_count']
            sk_price_bucket = stocks[sk]['price_bucket']
            sk_name = stocks[sk]['companyName']
            ### filtering
            if stocks[sk]['iex_unknown_symbol']:
                continue
            if sk_ct > OVERALL_LIMIT:
                continue
            if stocks[sk]['country'] not in DESIRED_COUNTRIES and DESIRED_COUNTRIES_LIMIT:
                continue
            if stocks[sk]['issueType'] not in DESIRED_STOCK_ISSUE_TYPE and DESIRED_STOCK_ISSUE_TYPE_LIMIT:
                continue
            if stocks[sk]['price_bucket'] not in DESIRED_PRICE_BUCKET and DESIRED_PRICE_BUCKET_LIMIT:
                continue
            if sk_history_count < MIN_HISTORY and MIN_HISTORY_LIMIT:
                continue
            if stocks[sk]['industry']  in NON_DESIRED_INDUSTRY and NON_DESIRED_INDUSTRY_LIMIT:
                continue
            if stocks[sk]['dividendYield'] < DIVIDEND_MIN and DIVIDEND_MIN_LIMIT:
                continue
            if stocks[sk]['peRatio'] > PE_MAX and PE_LIMIT:
                continue
        except:
            print('something is broke with extraction: ', sk_ct, sk)
            at.sys.exit(20)
        ### counting up filterd rows. 
        found_by_filter_ct += 1
        for t_item in stocks[sk]['tags']:
            if t_item in tags_ct:
                tags_ct[t_item] += 1
            else:
                tags_ct.update({t_item:1})
        if stocks[sk]['sector'] in sector_ct:
            sector_ct[stocks[sk]['sector']] += 1
        else:
            sector_ct.update({stocks[sk]['sector']:1})
        if stocks[sk]['country'] in country_ct:
            country_ct[stocks[sk]['country']] += 1
        else:
            country_ct.update({stocks[sk]['country']:1})
        if stocks[sk]['issueType'] in issueType_ct:
            issueType_ct[stocks[sk]['issueType']] += 1
        else:
            issueType_ct.update({stocks[sk]['issueType']:1})
        if sk_price_bucket in price_bucket_ct:
            price_bucket_ct[sk_price_bucket] += 1
        else:
            price_bucket_ct.update({sk_price_bucket:1})
        ### display
        if found_by_filter_ct < DISPLAY_LIMIT or found_by_filter_ct % DISPLAY_EVERY_NTH == 0:
            stock_row_print_format = '{0:<6}{1:<10}{2:<10}{3:<10}{4:<30}{5:<10}{6:<30}{7:<25}{8:<5}{9:<5}{10:<8}{11:<10}'
            try:
                print(stock_row_print_format.format(found_by_filter_ct, sk, sk_last_close, sk_history_count, 
                    sk_name[:28].encode("ascii", 'ignore').decode("ascii"), stocks[sk]['employees'], stocks[sk]['industry'][:28], 
                    stocks[sk]['sector'][:23], stocks[sk]['issueType'], 
                    stocks[sk]['country'], stocks[sk]['peRatio'], stocks[sk]['dividendYield']))
            except:
                print('FAIL, at printing', sk_ct, sk)
                at.sys.exit(20)
        ### check break file not every loop, but every so often
        if sk_ct % 10 == 0:
            if at.kill_file_check():
                break
    print('\nfound_by_filter_ct: ' + str(found_by_filter_ct))
    print('\ncountry_ct: ' + str(country_ct))
    print('\nissueType_ct:')
    for it in issueType_ct:
        print('\t{0:<5}{1:<10}{2}'.format(it, issueType_ct[it], at.iex_issue_type_code(it)))
    print('\nprice_bucket_ct:')
    for pb in price_bucket_ct:
        print('\t{0:<20}{1}'.format(pb, price_bucket_ct[pb]))
    # print('\n\n sector_ct: ' + str(sector_ct))
    # print('\n\n tags_ct: ' + str(tags_ct))
    print('')
    if TESTING:
        at.test_stock_data_file_save(stocks)
    else:
        at.stock_data_file_save(stocks)
    print('Time to process, ', round(at.datetime.now().timestamp() - stime, 2))
    

def main():
    at.kill_file_touch()
    list_all_company_info_basic()

  
if __name__== "__main__":
    main()
