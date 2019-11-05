import auto_trader as at


r_login_info = at.r_login()


user_profile = at.r_get_portfolio_profile()
print('unwithdrawable_deposits:   ' + user_profile['unwithdrawable_deposits'])
print('withdrawable_amount:       ' + user_profile['withdrawable_amount'])
print('excess_maintenance:        ' + user_profile['excess_maintenance'])
print('market_value:              ' + user_profile['market_value'])
print('equity:                    ' + user_profile['equity'])

user_account = at.r_get_build_user_profile()
print(user_account)

# last_bank_trans = None
# hours_since = None
# rh_account = None
# MIN_HOURS_BETWEEN_TRANSFERS = 3.0
# AUTO_DEPOSIT_AMOUNTS = 20
# print('\nbank transfers')
rh_bank_transfers = at.r_get_bank_transfers()
for rh_bank_trans in rh_bank_transfers:
    # if rh_bank_trans['direction'] == 'deposit' and not hours_since:
    #     rh_account = rh_bank_trans['account']
    #     hours_since = at.find_hours_since_epoch(
    #         at.human_to_epoch(human_time=rh_bank_trans['expected_landing_date'], str_format='%Y-%m-%d'))
    #     last_bank_trans = float(rh_bank_trans['amount'])
    rh_bank_trans.update({'scheduled_str': str(rh_bank_trans['scheduled'])})
    print(("""  sch:{0[scheduled_str]:<6} state:{0[state]:<15} amount:{0[amount]:<10} early:{0[early_access_amount]:<10} 
    direction:{0[direction]:<10} fees:{0[fees]:<10} landing:{0[expected_landing_date]:<15} 
    stat_desc:{0[status_description]:<10}""".format(rh_bank_trans)).replace('\n', ''))
# if hours_since > MIN_HOURS_BETWEEN_TRANSFERS:
#     print('Make a new deposit:')
#     print('  hours_since: ' + str(hours_since))
#     print('  last_bank_trans: ' + str(last_bank_trans))
#     print('  give me: ' + str(AUTO_DEPOSIT_AMOUNTS))




# s_earnings = at.r_get_stock_earnings('aal')
# for se in s_earnings:
#     print(se)
#     print('\n')

# s_fundamentals = at.r_get_stock_fundamentals('aal,a,aadr')
# for sf in get_fundamentals:
#     print(sf)
#     print('\n')

### did not reall work
# s_events = at.r_get_stock_events('aal,a,aadr')
# for se in s_events:
#     print(se)
#     print('\n')

### did not really work
# s_popularity = at.r_get_stock_popularity('aal,a,aadr')
# for sp in s_popularity:
#     print(sp)
#     print('\n')