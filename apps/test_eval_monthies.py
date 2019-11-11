import auto_trader as at
import calendar
import random

### TODO
# 1) Move buy sell logic into class                                         DONE
# 2) Find a way to dump transactions to disk for reporting
# 3) find a way to save overal all eval numbers to disk for reporting
# 4) Show volumes and include volumes into logic
# 5) find out whats up with the 1970 dates.
NUMBER_OF_RUNS = 100
at.kill_file_touch()

def save_data_to_file(mydata):
    fieldnames = sorted(mydata[0].keys())
    with open(at.define_monthly_eval_report_path(), 'w', newline='\n') as csvfile:
        d_writer = at.csv.DictWriter(csvfile, fieldnames=fieldnames)
        d_writer.writeheader()
        for data_row in mydata:
            d_writer.writerow(data_row)

my_monthly_eval = []

for run_num in range(NUMBER_OF_RUNS):
    print("\n################# STARTING RUN {0} ######################".format(run_num))
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
    # total_profit = 0

    close_epoch = None
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
            ### iterate over each day for the month.
            for m_day in range(last_day_for_month):
                today_is_the_day = str(starting_year + y_int) + '-' + str(m_int + 1).zfill(2) + '-' + str(m_day + 1).zfill(2)
                day_data = mth_history.iloc[mth_history.index.get_level_values('Date') == today_is_the_day].sort_values(by=['pct'], ascending=False)
                if day_data['Open'].count() == 0:
                    continue
                ### iterate over each stock for that day
                for index, row in day_data.iterrows():
                    ### split out two column index
                    close_date, SK = index
                    close_epoch = close_date.timestamp()
                    if SK in SKIP_STOCKS:
                        continue
                    my_account.stock_logic_one(close_date, close_epoch, SK, row)
            my_account.current_investment_prt(close_epoch=close_epoch, mount_count=loops)
            my_monthly_eval.append({
                'run_num': run_num,
                'loops': loops,
                'date_start': date_start,
                'amt_of_profit_for_sale': my_account.trans_logic_setting['AMT_OF_PROFIT'],
                'amnt_of_percent_slope_to_buy': my_account.trans_logic_setting['AMT_OF_PERCENT_CHANGE_TO_BUY'],
                'cash': my_account.account['cash'],
                'cash_deposits_total': my_account.account['cash_deposits_total'],
                'total_gain': my_account.account['total_gain'],
                'ownership_days_agv': my_account.account['ownership_days_agv'],
                'total_investments': my_account.account['total_investments'],
                'ct_owned': my_account.account['ct_owned'],
                'trades_sale': my_account.account['trades']['Sale'],
                'trades_buy': my_account.account['trades']['Buy']
            })
            save_data_to_file(my_monthly_eval)
            if at.kill_file_check():
                break
        # at.sleep(5)
        if at.kill_file_check():
            break
    print('Trading Months: ' + str(loops))
    print('Ending cash', my_account.account['cash'])
    # print('total_profit ', round(total_profit, 2))
    print('cash_deposits_total ', my_account.account['cash_deposits_total'])
    if at.kill_file_check():
        break
