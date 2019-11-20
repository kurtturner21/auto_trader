import auto_trader as at
import calendar
import random

my_account = at.sk_orders()
my_account.add_money(1000.00)
my_account.set_buffer(100.00)
my_account.set_amt_of_profit_requried_to_sale(round(random.random() * .5, 3))
my_account.set_amt_of_percent_change_to_buy(round(random.random() * .9, 3))
my_account.hide_each_transaction()
my_account.hide_all_still_invested()
print('Starting cash: ', my_account.account['cash'])

loops = 0
cash_deposits = 200
starting_year = random.randint(2000, 2018)
running_years = random.randint(2,5)
close_epoch = None
SKIP_STOCKS = ['pjt']
for y_int in range(running_years):
    for m_int in range(12):
        last_day_for_month = calendar.monthrange(starting_year + y_int, m_int+1)[1]
        date_start = at.datetime(starting_year + y_int, m_int+1, 1, 0, 0, 0)
        if date_start > at.datetime.now():
            break
        yyyy_mm_code = at.datetime.strftime(date_start, '%Y_%m')                                    ### creating a date code
        yr_mth_fpath = at.define_monthly_frames_history_path(yyyy_mm_code)
        mth_history = at.pd.read_csv(yr_mth_fpath, parse_dates=True, index_col=[0,1])
        ### iterate over each day for the month.
        for m_day in range(last_day_for_month):
            today_is_the_day = str(starting_year + y_int) + '-' + str(m_int + 1).zfill(2) + '-' + str(m_day + 1).zfill(2)
            day_data = mth_history.iloc[mth_history.index.get_level_values('Date') == today_is_the_day].sort_values(by=['pct'], ascending=False)
            if day_data['Open'].count() == 0:
                continue
            print(today_is_the_day)
