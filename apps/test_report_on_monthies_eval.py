import auto_trader as at
import calendar
import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import style
from datetime import timedelta
chart_window = 100


with open(at.define_eval_monthlies_transactions_path(), 'r', newline='\n') as csvfile:
    d_reader = at.csv.DictReader(csvfile)
    for trans_ct, trans in enumerate(d_reader):
        if trans_ct > 10:
            continue
        sk_file = at.define_stock_hist_path(trans['sk'])
        df_stock_history = at.pd.read_csv(sk_file, parse_dates=True, index_col=0)
        df_stock_history['52w_high'] =  round(df_stock_history['Adj Close'].rolling(window=52*5, min_periods=1).max(), 2)
        df_stock_history['52w_low'] =  round(df_stock_history['Adj Close'].rolling(window=52*5, min_periods=1).min(), 2)
        purchase_epoch = at.datetime.fromtimestamp(float(trans['purchase_epoch']))
        sale_epoch = at.datetime.fromtimestamp(float(trans['sale_epoch']))
        sale_epoch_plus_30 = sale_epoch + timedelta(days=30)
        purchase_epoch_minus_30 = purchase_epoch - timedelta(days=30)
        mask = (df_stock_history.index >= purchase_epoch_minus_30) & (df_stock_history.index < sale_epoch_plus_30)     ### creating a mast to filter the month
        print('{0:>5}) pur_date:{1[purchase_epoch]:<10}  sale_epoch:{1[sale_epoch]:<10}  profit:{1[profit]:<10} len: {1[ownership_len]:<10} amt_of_pct_gain_2buy: {1[amt_of_pct_gain_2buy]:<10} amt_of_proft_gain_2sale: {1[amt_of_proft_gain_2sale]:<10}'.format(trans_ct, trans))
        # print('{0:>5}) profit:{1[profit]:<10} len: {1[ownership_len]:<10} amt_of_pct_gain_2buy: {1[amt_of_pct_gain_2buy]:<10} amt_of_proft_gain_2sale: {1[amt_of_proft_gain_2sale]:<10}'.format(trans_ct, trans))
        # if int(trans['ownership_len']) > 1000:
        purchase_price = trans['purchase_price']

        df_to_plot = df_stock_history[mask] 
        linestyle = '-'
        style.use('ggplot')
        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.plot(df_to_plot.index, df_to_plot['Adj Close'],)
        ax1.plot(df_to_plot.index, df_to_plot['30ma'])
        # ax1.plot(df_to_plot.index, df_to_plot['100ma'])
        # ax1.plot(df_to_plot.index, df_to_plot['200ma'])
        ax1.plot(df_to_plot.index, df_to_plot['52w_high'])
        ax1.plot(df_to_plot.index, df_to_plot['52w_low'])
        ax1.axhline(y=purchase_price)
        ax1.axvline(x=purchase_epoch)
        ax1.axvline(x=sale_epoch)
        ax2.bar(df_to_plot.index, df_to_plot['Volume'])
        plt.show()