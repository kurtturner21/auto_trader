import auto_trader as at


# def populate_price_bucket():
#     TESTING = False
#     if TESTING:
#         stocks = at.test_stock_data_file_load()
#     else:
#         stocks = at.stock_data_file_load()
#     for st_ct, sk in enumerate(sorted(stocks)):
#         ### tempory
#         if 'Historicals' in stocks[sk]:
#             """ an example how to rename a key in a json file """
#             st_hist_path = stocks[sk].pop('Historicals')
#             stocks[sk].update({'Historicals_path': st_hist_path})
#         st_hist_path = stocks[sk]['Historicals_path']
#         new_path = at.define_stock_hist_path(sk)
#         if st_hist_path != new_path:
#             print(st_ct, sk, st_hist_path, new_path)
#             if at.os.path.isfile(st_hist_path):
#                 at.os.rename(st_hist_path, new_path)
#             stocks[sk]['Historicals_path'] = new_path
#     if TESTING:
#         at.test_stock_data_file_save(stocks)
#     else:
#         at.stock_data_file_save(stocks)

# def lower_case_stock_keys():
#     new_stocks = {}
#     stocks = at.stock_data_file_load()
#     for st_ct, sk in enumerate(sorted(stocks)):
#         new_sk = sk.lower()
#         print(st_ct, new_sk, sk)
#         new_stocks.update({
#             new_sk: stocks[sk]
#         })
#     at.stock_data_file_save(new_stocks)



def main():
    lower_case_stock_keys()

  
if __name__== "__main__":
    main()
