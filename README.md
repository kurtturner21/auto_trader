# auto_trader
 
## Daily processing steps

### Pull Down New Data

1. Manually download stock data from http://eoddata.com/download.aspx for AMEX, NYSE & NASDAQ in csv format and save it to \dev\auto_trader\eoddata\data_files\historicals\.
2. Open command prompt and chdir to \dev\auto_trader\eoddata
3. Run the python script to update data files with downloaded data:

    ```dos
    C:\dev\auto_trader\eoddata>python process_edo_data.py
    ```

Output looks like this:

```
C:\dev\auto_trader\eoddata>python process_edo_data.py
Stocks loaded: 9542
Processed histories loaded: 2427
Updated from stock lists: 8870
data_files\historicals\AMEX_20190814.csv AMEX 20190814 2219
data_files\historicals\AMEX_20190815.csv AMEX 20190815 2221
data_files\historicals\AMEX_20190816.csv AMEX 20190816 2217
data_files\historicals\AMEX_20190819.csv AMEX 20190819 2219
data_files\historicals\AMEX_20190821.csv AMEX 20190821 2213
data_files\historicals\AMEX_20190822.csv AMEX 20190822 2214
```

Time will take about 5 minutes.

### Populate price_bucket and some other status

Still in the command prompt, run this command.

```dos
C:\dev\auto_trader\apps>python edo_populate_price_bucket.py
```

This populates price_bucket, Historcials_file_exists, datecode_first, datecode_last, datecode_last_close & datecode_count in the stocks_list.json from the individual stock histories file.

Time will take about 5 minutes. 

#### Note

- The app has a feature to filter out duplicate data files.  The goal is to prevent duplicate dates getting into the stock CSV files.
- There exists STOCKS with no histories files.  Bug maybe?

## TODOs

### DONE
- https://iexcloud.io/docs/api/#key-stats
- https://iexcloud.io/docs/api/#news
- Setup a stock picker based off of interchangeable models
- http://www.robin-stocks.com/en/latest/
- robin_stocks.stocks.get_ratings(symbol, info=None)[source]
- Collabse "edo" & "iex" scripts down to one script.
- https://iexcloud.io/docs/api/#symbols
- remove current_and_usable from stocks data file.
- Last10K. - CIK

### in progress

- Setup a purchase tester for the picker with tracking cost bases, profit and lose, wash purchase warning, trade/day ratio limit, etc.

### Want to do

- https://iexcloud.io/docs/api/#historical-prices
- Reporting on purchase history.
- U.S. Holidays and Trading Dates
- Last10K. - Earnings
- https://iexcloud.io/docs/api/#splits  PAID
- https://iexcloud.io/docs/api/#price-target  PAID
