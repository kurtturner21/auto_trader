

# s_earnings = at.r_get_stock_earnings('aal')
# for se in s_earnings:
#     print(se)
#     print('\n')

# s_fundamentals = at.r_get_stock_fundamentals('aal,a,aadr')
# for sf in get_fundamentals:
#     print(sf)
#     print('\n')


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

