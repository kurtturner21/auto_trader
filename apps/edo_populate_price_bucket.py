import auto_trader as at
import codecs


def populate_price_bucket():
    TESTING = False
    DISPLAY_RATE = 1
    histrorial_file_de = {True:0, False: 0}
    current_and_usable = {True:0, False: 0}
    if TESTING:
        stocks = at.test_stock_data_file_load()
    else:
        stocks = at.stock_data_file_load()
    for st_ct, sk in enumerate(sorted(stocks)):
        ### temp
        # if sk != 'tsu':
        #     continue
        st_hist_path = stocks[sk]['Historicals_path']
        st_companyName = stocks[sk]['companyName']
        st_history = at.stock_history_load(st_hist_path)
        st_hist_file_exists = st_history['file_exists']
        st_history_datecode_first = ''
        st_history_datecode_last = ''
        st_history_datecode_last_close = ''
        st_history_datecode_count = 0
        p_bucket = ''
        histrorial_file_de[st_hist_file_exists] += 1
        if st_hist_file_exists:
            st_history_datecode_first = sorted(st_history['history_data'].keys())[0]
            st_history_datecode_last = sorted(st_history['history_data'].keys())[-1]
            st_history_datecode_last_close = float(st_history['history_data'][st_history_datecode_last]['Close'])
            st_history_datecode_count = len(st_history['history_data'].keys())
            p_bucket = at.define_stock_price_bucket(st_history_datecode_last_close)
        if st_ct % DISPLAY_RATE == 0:
            try:
                price_bucket_print_format = '{0:<5}{1:<7}{2:<60}{3:<10}{4:<10}{5:<10}{6:<10}{7:<10}{8:<10}'
                print(price_bucket_print_format.format(
                    st_ct, sk, ascii(str(st_companyName)),
                    st_history_datecode_first, st_history_datecode_last, st_history_datecode_count, 
                    st_history_datecode_last_close, p_bucket, st_hist_file_exists))
            except:
                print(st_ct, sk, st_companyName.ascii(),
                    st_history_datecode_first, st_history_datecode_last, st_history_datecode_count, 
                    st_history_datecode_last_close, p_bucket, st_hist_file_exists)
                at.sys.exit(20)
        stocks[sk]['price_bucket'] = p_bucket
        stocks[sk].update({'Historcials_file_exists':st_hist_file_exists}) 
        stocks[sk].update({'datecode_first':st_history_datecode_first}) 
        stocks[sk].update({'datecode_last':st_history_datecode_last}) 
        stocks[sk].update({'datecode_last_close':st_history_datecode_last_close}) 
        stocks[sk].update({'datecode_count':st_history_datecode_count}) 
        current_and_usable_question = False
        if st_history_datecode_count > 720 and at.get_date_code_latest() == st_history_datecode_last:
            stocks[sk].update({'current_and_usable':True})
            current_and_usable_question = True
        stocks[sk].update({'current_and_usable':current_and_usable_question})
        current_and_usable[current_and_usable_question] += 1
    if TESTING:
        at.test_stock_data_file_save(stocks)
    else:
        at.stock_data_file_save(stocks)
    print('histrorial_file does exists: ' + str(histrorial_file_de))
    print('current_and_usable: ' + str(current_and_usable))


def main():
    populate_price_bucket()

  
if __name__== "__main__":
    main()
