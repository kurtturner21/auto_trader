import auto_trader as at
import random
r_login_info = at.r_login()


OPENING_HOUR = 9
OPENING_MINUTE = 30
SLEEPING_SEC_BTW_LOOPS = 600
NO_AUTO_SALE_SYMBOLS = ['MOMO']


def list_all_company_info_basic():
    global picked_stocks
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
        # at.printing_stock_standard(found_by_filter_ct, stocks[sk], 'one')
        picked_stocks.append(sk)
    print('found_by_filter_ct: ' + str(found_by_filter_ct))
    print('country_ct: ' + str(country_ct))
    print('issueType_ct:')
    for it in issueType_ct:
        print('\t{0:<5}{1:<10}{2}'.format(it, issueType_ct[it], at.iex_issue_type_code(it)))
    print('price_bucket_ct:')
    for pb in price_bucket_ct:
        print('\t{0:<20}{1}'.format(pb, price_bucket_ct[pb]))
    # print('\n\n sector_ct: ' + str(sector_ct))
    # print('\n\n tags_ct: ' + str(tags_ct))
    print('Time to process, ', round(at.datetime.now().timestamp() - stime, 2))
    print('')


def show_user_profile():
    user_profile = at.r_get_portfolio_profile()
    print('unwithdrawable_deposits:   ' + user_profile['unwithdrawable_deposits'])
    print('withdrawable_amount:       ' + user_profile['withdrawable_amount'])
    print('excess_maintenance:        ' + user_profile['excess_maintenance'])
    print('market_value:              {0:<10}    {1:<10}  (extended)'.format(
        user_profile['market_value'], user_profile['extended_hours_market_value']))
    print('equity:                    {0:<10}    {1:<10}  (extended)'.format(
        user_profile['equity'], user_profile['extended_hours_equity']))
    print('CASH:                      ' + str(
        round(float(user_profile['equity']) - float(user_profile['market_value']), 4)
        ))

    print('\nBank Transfers')
    rh_bank_transfers = at.r_get_bank_transfers()
    for rh_bank_trans in rh_bank_transfers:
        rh_bank_trans.update({'scheduled_str': str(rh_bank_trans['scheduled'])})
        if rh_bank_trans['state'] in ('pending'):
            print(("""  sch:{0[scheduled_str]:<6} state:{0[state]:<15} amount:{0[amount]:<10} early:{0[early_access_amount]:<10} 
            direction:{0[direction]:<10} fees:{0[fees]:<10} landing:{0[expected_landing_date]:<15} 
            stat_desc:{0[status_description]:<10}""".format(rh_bank_trans)).replace('\n', ''))


def nap_time(current_time, do_exit):
    if current_time.hour >= 16:
        print('Market has closed - break out of application.')
        do_exit = True
    elif current_time.hour <= OPENING_HOUR and current_time.minute < OPENING_MINUTE:
        print('Market has not opened yet.  Witing...')
        while current_time.hour <= OPENING_HOUR and current_time.minute < OPENING_MINUTE:
            current_time = at.datetime.now()
            at.sleep(5)
            do_exit = at.kill_file_check()
            if do_exit:
                break
    else: 
        sleeping_mod = 5
        for my_sleep in range(int(SLEEPING_SEC_BTW_LOOPS / sleeping_mod)):
            at.sleep(sleeping_mod)
            do_exit = at.kill_file_check()
            if do_exit:
                break
    return do_exit


def show_user_holding_and_orders(holding_check_ct, current_str_time):
    user_holdings = at.r_get_build_user_holdings()
    user_profile = at.r_get_portfolio_profile()
    print('\n\nHoldings---- ({0})    {1}  {2}'.format(holding_check_ct, current_str_time, user_profile['equity']))
    for uh_symbol in user_holdings:
        this_holding = user_holdings[uh_symbol]
        this_holding.update({'price': round(float(this_holding['price']), 3)})
        this_holding.update({'quantity': round(float(this_holding['quantity']), 3)})
        this_holding.update({'equity_change': round(float(this_holding['equity_change']), 3)})
        this_holding.update({'pe_ratio': round(float(this_holding['pe_ratio']), 3)})
        this_holding.update({'average_buy_price': round(float(this_holding['average_buy_price']), 3)})
        this_holding.update({'profitloss': round((
            float(this_holding['equity']) - 
            (this_holding['average_buy_price'] * this_holding['quantity'])
            ), 3)})
        sale_price = 0.0
        sale_price_should_be = round(float(this_holding['average_buy_price'] * 1.1), 2)
        sale_qty_should_be = this_holding['quantity'] - 1
        has_orders = False
        cancel_order_detail = None
        order_details = ''
        ### gathering stock orders
        symbol_orders = at.r_get_orders_for_symbol(uh_symbol)
        for syb_order in symbol_orders:
            syb_order['stop_price'] = str(syb_order['stop_price'])
            if not syb_order['price']:
                syb_order['price'] = 0
            syb_order['price'] = round(float(syb_order['price']), 3)
            syb_order['created_at'] = str(syb_order['created_at']).split('T')[0]
            syb_order['updated_at'] = str(syb_order['updated_at']).split('T')[0]
            order_id = syb_order['id']
            ### don't care about seeing cancelled orders
            if syb_order['state'] == 'cancelled':
                continue
            ### don't care about buy orders...  The user_holding gives all the stats I need.
            if syb_order['side'] == 'buy':
                continue
            has_orders = True
            sale_price = syb_order['price']
            if sale_price > sale_price_should_be and uh_symbol not in NO_AUTO_SALE_SYMBOLS:
                cancel_url = syb_order['cancel']
                if syb_order['executions']:
                    cancel_url = syb_order['url'] + 'cancel/'
                cancel_order_detail = at.r_get_stock_cancel_order(cancel_url)['detail']
            order_details += ("""     side:{0[side]:<6}  quantity:{0[quantity]:<6}  price:{0[price]:<6} """.format(syb_order)).replace('\n', '')
        print(("""  {1:<6}  price b:{0[price]:<6} s:{2:<6} qty:{0[quantity]:<5} agv_buy:{0[average_buy_price]:<9} pe_ratio:{0[pe_ratio]:<8}  eq:{0[equity]:<10} {0[percent_change]:>8} %  ${0[profitloss]:8} 
        """.format(this_holding, uh_symbol, sale_price)).replace('\n', ''))
        if order_details:
            print(order_details)
        if cancel_order_detail:
            print('     cancel detail: ' + str(cancel_order_detail))
        if sale_price == 0.0 and has_orders == False:
            print('     THIS STOCK NEEDS AN ORDER TO BE CREATED - need to sell {0} target at {1}. '.format(sale_qty_should_be, sale_price_should_be))
            order_data = at.r_post_create_order(uh_symbol, sale_price_should_be, sale_qty_should_be)
            print(order_data)



def main():
    ### declare vars
    is_testing = True
    do_exit = False
    holding_check_ct = 0 
    global picked_stocks
    picked_stocks = []
    ### start app
    at.kill_file_touch()
    list_all_company_info_basic()
    show_user_profile()
    while not do_exit:
        current_time = at.datetime.now()
        current_str_time = at.datetime.now().strftime("%m/%d/%Y %H:%M")
        holding_check_ct += 1
        show_user_holding_and_orders(
            holding_check_ct=holding_check_ct,
            current_str_time=current_str_time
            )
        print('random picker', random.choice(picked_stocks))
        if not is_testing:
            do_exit = nap_time(
                do_exit=do_exit,
                current_time=current_time,
                )
        else:
            do_exit = True



if __name__== "__main__":
    main()
