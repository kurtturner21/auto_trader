# auto_trader

 
## Daily processing steps

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

### Note

- The app has a feature to filter out duplicate data files.  The goal is to prevent duplicate dates getting into the stock CSV files.