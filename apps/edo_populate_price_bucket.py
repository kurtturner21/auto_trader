import auto_trader_common as at


def populate_price_bucket():
    stocks = at.stock_data_file_load()
    for st_ct, sk in enumerate(sorted(stocks)):
        if st_ct > 30: 
            break
        if 'Historicals_path' in stocks[sk]:
            highest_price_100d = at.get_highest_historial_price(100, stocks[sk]['Historicals_path'])['highest_price']
            highest_price_200d = at.get_highest_historial_price(200, stocks[sk]['Historicals_path'])['highest_price']
            price_bucket_print_format = '{0:<5}{1:<7}{2:<60}{3:<10}{4:<10}'
            print(price_bucket_print_format.format(st_ct, sk, stocks[sk]['Description'], 
                highest_price_100d, highest_price_200d))


def main():
    populate_price_bucket()

  
if __name__== "__main__":
    main()
