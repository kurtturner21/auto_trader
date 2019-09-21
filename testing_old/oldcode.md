### cut out of list_company_info

```python
    ## extracting from stock key facts:
    if sk_hrs_since_iex_key_facts > 1000 or 'peRatio' not in stocks[sk_symbol]:
        sk_key_facts = at.iex_stock_get_key_facts(sk_symbol)
        sk_key_facts['data'] = at.iex_stock_key_facts_fix(sk_key_facts['data'])
        if sk_key_facts['api_call']:
            api_call_count += 1
            if api_call_count % SLEEP_TIME_OUT_ON_IEX == 0:
                ### take time to save data and sleep
                print('take time to save data and sleep, api_call_count:' + str(api_call_count))
                at.stock_data_file_save(stocks)
                at.iex_account_metadata_display()
                sleep(5)
        stocks[sk_symbol].update({
            'iex_key_facts_epoch': at.generate_effective_epoch(),
            "iex_key_facts_path": sk_key_facts["file_path"]
        }) 
        ### adding to stocks:
        stocks[sk_symbol].update({'peRatio': sk_key_facts['data']['peRatio']})
        stocks[sk_symbol].update({'dividendYield': sk_key_facts['data']['dividendYield']})
```

more code

```python
    sk_hrs_since_iex_comp_info = at.find_hours_since_epoch(stocks[sk_symbol], 'iex_company_info_effect_epoch')
    sk_hrs_since_iex_key_facts = at.find_hours_since_epoch(stocks[sk_symbol], 'iex_key_facts_epoch')
    ### extracting from company_data: 
    ### would like to move this to processing script.
    if sk_hrs_since_iex_comp_info > 1000 or 'iex_unknown_symbol' not in stocks[sk_symbol]:
        company_info = at.iex_stock_company_get_info(sk_symbol)
        company_info_data = at.iex_stock_company_fix_info(company_info['data'])
        stocks[sk_symbol].update({'employees': company_info_data['employees']})
        stocks[sk_symbol].update({'tags': company_info_data['tags']})
        stocks[sk_symbol].update({'industry': company_info_data['industry']})
        stocks[sk_symbol].update({'sector': company_info_data['sector']})
        stocks[sk_symbol].update({'issueType': company_info_data['issueType']})
        stocks[sk_symbol].update({'country': company_info_data['country']})
        stocks[sk_symbol].update({'iex_unknown_symbol': company_info['unknown_symbol']})
    ### cleaning - Temporary
    stocks[sk_symbol] = at.kill_dict_key(stocks[sk_symbol], 'iex_company_info_path')
    if not stocks[sk_symbol]['country']:
        stocks[sk_symbol]['country'] = ''
    if not stocks[sk_symbol]['industry']:
        stocks[sk_symbol]['industry'] = ''
```

some api stuff

```python
    SLEEP_TIME_OUT_ON_IEX = 200
    api_call_count = 0
    at.iex_account_metadata_display()
    at.iex_unknown_symbols_load()
    at.iex_account_metadata_display()
    print('IEX api_call_count: ' + str(api_call_count))
```