import auto_trader_common as at

def evaluate_duplicates():
    PRINT_DAYILY_STATS = False
    PRINT_DUPLICATE_MESSAGE = False
    MAX_REC_PROCESS_CT_TO_PRINT = 10
    MAX_HIST_DAY_CT_TO_PRINT = 4
    stocks = at.stock_data_file_load()
    for st_ct, sk in enumerate(sorted(stocks)):
        hist_path = ''
        daily_count = 0
        duplicate_count = 0
        new_history_data = []
        d_reader_fields = None
        if 'Historicals_path' in stocks[sk]:
            hist_path = stocks[sk]['Historicals_path']
        if st_ct > MAX_REC_PROCESS_CT_TO_PRINT: 
            break
        if PRINT_DAYILY_STATS:
            print(stocks[sk])
        if hist_path:
            if at.os.path.isfile(hist_path):
                with open(hist_path, 'r') as csvfile:
                    d_reader = at.csv.DictReader(csvfile)
                    date_set = set()
                    d_reader_fields = d_reader.fieldnames
                    for td_ct, trade_day in enumerate(d_reader):
                        daily_count += 1
                        if td_ct < MAX_HIST_DAY_CT_TO_PRINT and PRINT_DAYILY_STATS: 
                            print('\t' + str(trade_day))
                        trade_day_date = trade_day['Date']
                        if trade_day_date in date_set:
                            duplicate_count += 1
                            if PRINT_DUPLICATE_MESSAGE:
                                print('\t\tduplicate found ' + trade_day_date)
                        else:
                            new_history_data.append(trade_day)
                        date_set.add(trade_day_date)
            else:
                print('\tfile does not exist' + hist_path)
        else:
            print('\tHistoricals_path key does not exist')
        stock_status_print_format_str = "{0:<5}{1:<5}{2:<40}day ct:{3:<5} dup ct:{4:<5}"
        print(stock_status_print_format_str.format(st_ct, sk, hist_path, 
            daily_count, duplicate_count))
        if duplicate_count > 0 and d_reader_fields:
            with open(hist_path, 'w') as csvfile:
                writer = at.csv.DictWriter(csvfile, fieldnames=d_reader_fields)
                writer.writeheader()
                for data_out in new_history_data:
                    writer.writerow(data_out)


def main():
    evaluate_duplicates()

  
if __name__== "__main__":
    main()
