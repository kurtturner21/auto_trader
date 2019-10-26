import auto_trader as at
import math

MAX_LAST_LEN = 5        ### number of days to look at trends.  
AMT_OF_PROFIT = .1      ### percent of profit to gain before selling a stock
AMT_OF_PERCENT_CHANGE_TO_BUY = .1  ### The slope of percent chnage before purchage can happen
DAY_OF_PERCENT_GAIN = 30 ### the number of days for AMT_OF_PERCENT_CHANGE_TO_BUY to gain.  


def run_module_one(SK, starting_test_date):
    global my_account
    sk_file = at.define_stock_hist_path(SK)
    df_stock_history = at.pd.read_csv(sk_file, parse_dates=True, index_col=0)
    # df_stock_history['nd_min'] =  round(df_stock_history['Adj Close'].rolling(window=MAX_LAST_LEN, min_periods=MAX_LAST_LEN).min(), 2)
    # df_stock_history['nd_max'] =  round(df_stock_history['Adj Close'].rolling(window=MAX_LAST_LEN, min_periods=MAX_LAST_LEN).max(), 2)
    # df_stock_history['pctn'] =  round(df_stock_history['Adj Close'].pct_change(periods=MAX_LAST_LEN), 2)
    df_stock_history['nma'] =  round(df_stock_history['Adj Close'].rolling(window=MAX_LAST_LEN, min_periods=MAX_LAST_LEN).mean(), 2)
    df_stock_history['pct'] =  round(df_stock_history['Adj Close'].pct_change(periods=DAY_OF_PERCENT_GAIN), 2)
    s_profit = 0
    s_invested = 0
    date_purchase = None
    date_sold = None
    r_close = 0
    waiting_days = 0
    for index, row in df_stock_history.iterrows():
        # fast forward up to the point of last stock sold. 
        if index < starting_test_date:
            continue
        waiting_days += 1
        # don't want to wait too long.  
        if waiting_days > 100:
            break
        r_close = round(row['Adj Close'], 2)
        r_nma= round(row['nma'], 2)
        r_pct = round(row['pct'], 2)
        date_sold = index
        if date_purchase is None and r_close < r_nma and r_pct > AMT_OF_PERCENT_CHANGE_TO_BUY:
            date_purchase = index
            my_account.buy_stock(SK, r_close, at.human_to_epoch(str(index)))
            s_profit = my_account.current_profit(SK, r_close)
            s_invested = my_account.current_invested(SK)
        elif date_purchase is not None and r_close < r_nma:
            s_invested = my_account.current_invested(SK)
            s_profit = my_account.current_profit(SK, r_close)
            if s_profit > (s_invested * AMT_OF_PROFIT):
                break
    if date_purchase is not None:
        my_account.sale_stock(SK, r_close, at.human_to_epoch(str(date_sold)))
    return date_sold, date_purchase


def main():
    global my_account 
    my_account = at.sk_orders()
    my_account.add_money(1000.00)
    my_account.set_buffer(100.00)
    starting_test_date = at.datetime(2000, 1, 1, 0, 0, 0)
    print('Starting cash: ', my_account.account['cash'])
    print('Starting test date: ', starting_test_date)
    for given_sk in ('adi', 'afya', 'exiv', 'pgti'):
        date_sold, date_purchase = run_module_one(given_sk, starting_test_date)
        print(given_sk, date_purchase, date_sold)
        starting_test_date = date_sold
    my_account.order_history_prt()
    print('Ending cash', my_account.account['cash'])


  
if __name__== "__main__":
    main()



