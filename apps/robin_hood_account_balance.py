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