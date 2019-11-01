import auto_trader as at
import calendar
import random

MAX_LAST_LEN = 5        ### number of days to look at trends.  
AMT_OF_PROFIT = .01      ### percent of profit to gain before selling a stock
AMT_OF_PERCENT_CHANGE_TO_BUY = .2  ### The slope of percent chnage before purchage can happen
DAY_OF_PERCENT_GAIN = 30 ### the number of days for AMT_OF_PERCENT_CHANGE_TO_BUY to gain.  

### TODO
# 1) Move buy sell logic into class
# 2) Add paramaters to script for above constants
# 3) Find a way to dump transactions to disk for reporting
# 4) find a way to show overal all eval numbers to disk for reporting
# 5) Show volumes and include volumes into logic

my_account = at.sk_orders()
my_account.add_money(1000.00)
my_account.set_buffer(100.00)
# my_account.hide_each_transaction()
my_account.hide_all_still_invested()
print('Starting cash: ', my_account.account['cash'])

loops = 0
cash_deposits = 200
starting_year = random.randint(2000, 2018)
running_years = random.randint(1,2)
total_profit = 0

close_epoch = None
at.kill_file_touch()
SKIP_STOCKS = ['pjt']
for y_int in range(running_years):
    for m_int in range(12):
        # print('Added CASH ', cash_deposits)
        # print('cash_deposits_total ', my_account.account['cash_deposits_total'])
        loops += 1
        my_account.add_money(cash_deposits)
        last_day_for_month = calendar.monthrange(starting_year + y_int, m_int+1)[1]
        date_start = at.datetime(starting_year + y_int, m_int+1, 1, 0, 0, 0)
        if date_start > at.datetime.now():
            break
        yyyy_mm_code = at.datetime.strftime(date_start, '%Y_%m')                                    ### creating a date code
        yr_mth_fpath = at.define_monthly_frames_history_path(yyyy_mm_code)
        mth_history = at.pd.read_csv(yr_mth_fpath, parse_dates=True, index_col=[0,1])
        for m_day in range(last_day_for_month):
            today_is_the_day = str(starting_year + y_int) + '-' + str(m_int + 1).zfill(2) + '-' + str(m_day + 1).zfill(2)
            day_data = mth_history.iloc[mth_history.index.get_level_values('Date') == today_is_the_day].sort_values(by=['pct'], ascending=False)
            if day_data['Open'].count() == 0:
                continue
            for index, row in day_data.iterrows():
                close_date, SK = index
                if SK in SKIP_STOCKS:
                    continue
                close_epoch = close_date.timestamp()
                r_close = round(row['Adj Close'], 2)
                r_nma= round(row['nma'], 2)
                r_pct = round(row['pct'], 2)
                if SK not in my_account.current_orders and r_close < r_nma and r_pct > AMT_OF_PERCENT_CHANGE_TO_BUY:
                    if my_account.account['cash'] > (my_account.account['buffer'] + r_close):
                        my_account.buy_stock(SK, r_close, close_epoch)
                elif SK in my_account.current_orders:
                    s_invested = my_account.current_invested(SK)
                    s_profit = my_account.current_profit(SK, r_close)
                    if s_profit > (s_invested * AMT_OF_PROFIT):
                        my_account.sale_stock(SK, r_close, close_epoch)
                        total_profit += s_profit
        my_account.current_investment_prt(close_epoch=close_epoch, mount_count=loops)
        if at.kill_file_check():
            break
    # at.sleep(5)
    if at.kill_file_check():
        break
print('\n')
print('Trading Months: ' + str(loops))
print('Ending cash', my_account.account['cash'])
print('total_profit ', round(total_profit, 2))
print('cash_deposits_total ', my_account.account['cash_deposits_total'])

