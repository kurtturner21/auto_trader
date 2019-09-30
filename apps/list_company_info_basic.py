import auto_trader as at

def list_all_company_info_basic():
    stime = at.datetime.now().timestamp()
    TESTING = at.get_run_in_testing()
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
    ### starting to loop over stocks 
    for sk in sorted(stocks):
        if at.filter_me(stocks[sk]):
            continue
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
        if stocks[sk]['price_bucket'] in price_bucket_ct:
            price_bucket_ct[stocks[sk]['price_bucket']] += 1
        else:
            price_bucket_ct.update({stocks[sk]['price_bucket']:1})
        at.printing_stock_standard(found_by_filter_ct, stocks[sk], 'one')
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
    print('Time to process, ', round(at.datetime.now().timestamp() - stime, 2))
    

def main():
    list_all_company_info_basic()

  
if __name__== "__main__":
    main()
