import auto_trader as at


def evaluate_duplicates():
    MAX_REC_PROCESS_CT_TO_PRINT = 10000
    stocks = at.stock_data_file_load()
    for st_ct, sk in enumerate(sorted(stocks)):
        st_hist_path = stocks[sk]['Historicals_path']
        st_history = at.stock_history_load(st_hist_path)
        st_history_datecode_count = len(st_history['history_data'].keys())
        if st_ct > MAX_REC_PROCESS_CT_TO_PRINT: 
            break
        stock_status_print_format_str = "{0:<5}{1:<10}{2:<100}day ct:{3:<5} dup ct:{4:<5}"
        print(stock_status_print_format_str.format(st_ct, sk, st_hist_path, 
            st_history_datecode_count, ''))
        at.stock_history_save(st_history)


def main():
    evaluate_duplicates()

  
if __name__== "__main__":
    main()
