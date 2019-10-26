import auto_trader as at
import matplotlib.pyplot as plt
from matplotlib.pyplot import style


SK = at.sys.argv[1]
chart_window = int(at.sys.argv[2])
sk_file = at.define_stock_hist_path(SK)
df_stock_history = at.pd.read_csv(sk_file, parse_dates=True, index_col=0)

# print(stocks[SK])

# df_stock_history['52w_high'] =  round(df_stock_history['Adj Close'].rolling(window=52*5, min_periods=1).max(), 2)
# df_stock_history['52w_low'] =  round(df_stock_history['Adj Close'].rolling(window=52*5, min_periods=1).min(), 2)
# df_stock_history['pct'] =  round(df_stock_history['Adj Close'].pct_change(periods=1), 2)
# df_stock_history['pct5'] =  round(df_stock_history['Adj Close'].pct_change(periods=5), 2)
# df_stock_history['pct30'] =  round(df_stock_history['Adj Close'].pct_change(periods=30), 2)
# df_stock_history['200ma'] =  round(df_stock_history['200ma'], 2)
# df_stock_history['pct_mid'] =  0

### figure out buy and selling logic
cash = 1000.0
buffer = 100
state = 'Sale'
buy_price = 0
share_count = 0
profit = 0
invested = 0
trades = {'Sale': 0, 'Buy': 0}
run_count = 0
for index, row in df_stock_history.tail(chart_window).iterrows():
    row['Close'] = round(row['Close'], 2)
    # if state == 'sell' and row['200ma'] > row['Close'] and row['pct'] > row['pct5'] and row['200ma'] > 0 and (cash - buffer) > row['Close']:
    # if state == 'Sale' and (cash - buffer) > row['Close'] and row['200ma'] > row['Close']:
    if state == 'Sale' and (cash - buffer) > row['Close'] and run_count > 20:
        state = 'Buy'
        trades[state] += 1
        buy_price = row['Close']
        share_count = int((cash - buffer) / buy_price)
        invested = round((share_count * buy_price), 2)
        cash = round(cash - (share_count * buy_price), 2)
        run_count = 0
    elif state == 'Buy' and profit > invested*0.1:
        state = 'Sale'
        trades[state] += 1
        cash = round(cash + (share_count *  row['Close']), 2)
        invested = 0
        buy_price = 0
        share_count = 0
        run_count = 0
    else:
        run_count = 0
    profit = round((row['Close'] - buy_price) * share_count, 2)
    account_value = round(((row['Close'] * share_count) + cash), 2)
    # print('{0:<8} 52h:{1:<8} 52l:{2:<8} 200ma:{3:<8} p5: {4:<8} p30: {5:<8}{6:<10}\t\t{7:>10}{8:>10}{9:>10}{10:>10} tot:{11:>10} inv:{12:>10}'.format(
    #     row['Close'], row['52w_high'], row['52w_high'], row['200ma'], row['pct5'], row['pct30'], state,
    #     cash, buy_price, share_count, profit, account_value, invested))
print(account_value, trades)


# df_to_plot = df_stock_history[-chart_window:]
# ### chart two
# linestyle = '-'
# style.use('ggplot')
# plt.plot(df_to_plot.index, df_to_plot['Close'])
# plt.plot(df_to_plot.index, df_to_plot['52w_high'])
# plt.plot(df_to_plot.index, df_to_plot['52w_low'])
# plt.plot(df_to_plot.index, df_to_plot['200ma'], linestyle=linestyle)
# plt.plot(df_to_plot.index, df_to_plot['30ma'], linestyle=linestyle)
# plt.show()

# ### chart one
# print(df_to_plot[['Adj Close','pct','pct5','pct30']].tail(30))
# style.use('ggplot')
# ax1 = plt.subplot2grid((11,1), (0,0), rowspan=5, colspan=1)
# ax2 = plt.subplot2grid((11,1), (5,0), rowspan=5, colspan=1, sharex=ax1)
# ax3 = plt.subplot2grid((11,1), (10,0), rowspan=1, colspan=1, sharex=ax1)
# ax1.plot(df_to_plot.index, df_to_plot['Adj Close'],)
# ax1.plot(df_to_plot.index, df_to_plot['30ma'])
# ax1.plot(df_to_plot.index, df_to_plot['100ma'])
# ax1.plot(df_to_plot.index, df_to_plot['200ma'])
# ax1.plot(df_to_plot.index, df_to_plot['52w_high'])
# ax1.plot(df_to_plot.index, df_to_plot['52w_low'])
# ax2.plot(df_to_plot.index, df_to_plot['pct'])
# ax2.plot(df_to_plot.index, df_to_plot['pct5'])
# ax2.plot(df_to_plot.index, df_to_plot['pct30'])
# ax2.plot(df_to_plot.index, df_to_plot['pct_mid'])
# ax3.bar(df_to_plot.index, df_to_plot['Volume'])
# plt.show()




        # elif purchase_state == 'buy':
        #     s_profit = my_account.current_profit(SK, r_close)
        # cur_total = round(my_account.account['cash'] + s_profit + s_invested, 2)
        # print('c:{0:<8} nma:{1:<5} {2:<6} pur: {3:<10} ct: {4:<5}  pft: {5:>8}   cash: {6:>8}   inv: {7:>8}   tot:  {8:<10}'.format(
        #     r_close, r_nma, purchase_state, 
        #     purchase_price, 
        #     share_count, 
        #     s_profit, 
        #     my_account.account['cash'], 
        #     s_invested, 
        #     cur_total
        #     ))
    # style.use('ggplot')
    # plt.plot(df_stock_history.index, df_stock_history['Adj Close'])
    # plt.plot(df_stock_history.index, df_stock_history['nd_min'])
    # plt.plot(df_stock_history.index, df_stock_history['nd_max'])
    # plt.plot(df_stock_history.index, df_stock_history['nma'])
    # plt.show()