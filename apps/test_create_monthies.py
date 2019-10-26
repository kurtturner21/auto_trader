import auto_trader as at
import calendar
import random

MAX_LAST_LEN = 5        ### number of days to look at trends.  
AMT_OF_PROFIT = .1      ### percent of profit to gain before selling a stock
AMT_OF_PERCENT_CHANGE_TO_BUY = .1  ### The slope of percent chnage before purchage can happen
DAY_OF_PERCENT_GAIN = 30 ### the number of days for AMT_OF_PERCENT_CHANGE_TO_BUY to gain.  

TESTING = at.get_run_in_testing()
if TESTING:
    stocks = at.test_stock_data_file_load()
else:
    stocks = at.stock_data_file_load()
stks_to_gather = {}
for sk_sym in stocks:
    if at.filter_for_pulling_stock_histories(stocks[sk_sym]):
        continue
    sk_file = at.define_stock_hist_path(sk_sym)
    if not at.os.path.isfile(sk_file):
        continue
    try:
        df_stock_history = at.pd.read_csv(sk_file, parse_dates=True, index_col=0)
    except:
        print('error with ', sk_sym)
        continue
    stks_to_gather.update({sk_sym:df_stock_history})
print(len(stks_to_gather.keys()))

loops = 0
for y_int in range(20):
    for m_int in range(12):
        last_day_for_month = calendar.monthrange(2000 + y_int, m_int+1)[1]
        date_start = at.datetime(2000 + y_int, m_int+1, 1, 0, 0, 0)
        date_end = at.datetime(2000 + y_int, m_int+1, last_day_for_month, 23, 59, 59)
        df_mth = []
        for sk_sym in stks_to_gather:
            loops += 1
            history_count = 0
            history_count_masked = 0
            df_stock_history = stks_to_gather[sk_sym]
            history_count = df_stock_history['Open'].count()
            #### the follow two lines are needed  --  work into ingesting script
            df_stock_history['nma'] =  round(df_stock_history['Close'].rolling(window=MAX_LAST_LEN, min_periods=MAX_LAST_LEN).mean(), 2)
            df_stock_history['pct'] =  round(df_stock_history['Close'].pct_change(periods=DAY_OF_PERCENT_GAIN), 2)
            ####
            df_stock_history['sk'] = sk_sym  ### adding the symbol as a column
            mask = (df_stock_history.index >= date_start) & (df_stock_history.index < date_end)     ### creating a mast to filter the month
            df_mth_sk = df_stock_history[mask]                                                      ### getting the sub set
            df_mth_sk.set_index(['sk'], inplace=True, append=True, drop=False)                      ### making the symbol a index
            history_count_masked = df_mth_sk['Open'].count()
            df_mth.append(df_mth_sk)                                                        ### creating a list of df pointers
            # print('found error with ', sk_sym, date_start, sk_file, history_count, history_count_masked)
        df_mth_all = at.pd.concat(df_mth)                                                           ### adding all the frames together
        yyyy_mm_code = at.datetime.strftime(date_start, '%Y_%m')                                    ### creating a date code
        yr_mth_fpath = at.define_monthly_frames_history_path(yyyy_mm_code)
        df_mth_all.to_csv(yr_mth_fpath)
        print('finished with ' + yr_mth_fpath)
