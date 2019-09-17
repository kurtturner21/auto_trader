import auto_trader as at
from time import sleep


def recover_from_stock_histories():
    SLEEP_TIME_OUT_ON_IEX = 100
    api_call_count = 0
    at.iex_account_metadata()
    at.iex_unknown_symbols_load()
    stocks = at.stock_data_file_load()
    all_stock_histories = at.list_all_stock_histories()
    print('This many stocks files found: ' + str(len(all_stock_histories)))
    print('------------------------------')
    sleep(20)
    for sp_ct, s_path in enumerate(all_stock_histories):
        if sp_ct > 10000:
            break
        sk_symbol = at.get_stock_symbol_from_path(s_path)
        in_stocks = False
        if sk_symbol in stocks:
            in_stocks = True
        if not in_stocks:
            print(sp_ct, s_path, sk_symbol, in_stocks)
            stocks.update({
                sk_symbol: at.create_stock_lists_stock(sk_symbol)
                })
            company_data = at.iex_stock_company_get_info(sk_symbol)
            if company_data['api_call']:
                api_call_count += 1
                if api_call_count % SLEEP_TIME_OUT_ON_IEX == 0:
                    ### take time to save data and sleep
                    print('take time to save data and sleep, api_call_count:' + str(api_call_count))
                    at.stock_data_file_save(stocks)
                    sleep(5)
            stocks[sk_symbol].update({
                "iex_company_info_path": company_data["file_path"], 
                "iex_company_info_effect_epoch": at.generate_effective_epoch(),
                "Historcials_file_exists": True
                })
            for iex_key in ['companyName', 'exchange', 'industry']:
                iex_key_data = None
                if iex_key in company_data['data']:
                    iex_key_data = company_data['data'][iex_key]
                stocks[sk_symbol].update({iex_key: iex_key_data})
    at.stock_data_file_save(stocks)
    

def main():
    recover_from_stock_histories()

  
if __name__== "__main__":
    main()
