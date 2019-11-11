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

print('\nBank Transfers')
rh_bank_transfers = at.r_get_bank_transfers()
for rh_bank_trans in rh_bank_transfers:
    rh_bank_trans.update({'scheduled_str': str(rh_bank_trans['scheduled'])})
    print(("""  sch:{0[scheduled_str]:<6} state:{0[state]:<15} amount:{0[amount]:<10} early:{0[early_access_amount]:<10} 
    direction:{0[direction]:<10} fees:{0[fees]:<10} landing:{0[expected_landing_date]:<15} 
    stat_desc:{0[status_description]:<10}""".format(rh_bank_trans)).replace('\n', ''))


# print('\nAccount Documents - BROKEN')
# file_downloaded_count = 0
# rh_account_documents = at.r_get_account_documents()
# for rh_doc in rh_account_documents:
#     rh_doc.update({'is_from_rhs_str': str(rh_doc['is_from_rhs'])})
#     if rh_doc['type'] == 'trade_confirm':
#         f_path_dir = at.get_document_stor_trade_confirm() + '\\'
#         f_path_name = rh_doc['date'] + '-' + rh_doc['id']
#     else:
#         f_path_dir = at.get_document_stor_account_statements() + '\\'
#         f_path_name = rh_doc['date'] + '-' + rh_doc['type']
#     f_path = at.os.path.join(f_path_dir, f_path_name + '.' + rh_doc['filetype'])
#     if not at.os.path.isfile(f_path):
#         file_downloaded_count += 1
#         print((""" {0:>3}) f_rhs:{1[is_from_rhs_str]:<6} date:{1[date]:<15} filetype:{1[filetype]:<10} type:{1[type]:<10}
#         """.format(file_downloaded_count, rh_doc)).replace('\n', ''))
#         at.r_get_account_download_document(rh_doc['url'], f_path_name, f_path_dir)
# print('files downloaded: ' + str(file_downloaded_count))



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