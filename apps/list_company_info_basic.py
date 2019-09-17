import auto_trader as at


def list_all_company_info_basic():
    at.iex_unknown_symbols_load()
    stocks = at.stock_data_file_load()
    country_ct = {}
    issueType_ct = {}
    sector_ct = {}
    tags_ct = {}
    for sp_ct, sk_symbol in enumerate(sorted(stocks)):
        company_data = at.iex_stock_company_get_info(sk_symbol, False)
        if company_data['unknown_symbol']:
            continue
        comp_employees = ''
        comp_tags = ''
        comp_ceo = ''
        comp_industry = ''
        comp_sector = ''
        comp_issueType = ''
        comp_website = ''
        comp_country = ''
        if 'employees' in company_data['data']:
            comp_employees = company_data['data']['employees']
        if 'tags' in company_data['data']:
            comp_tags = company_data['data']['tags']
            for t_item in comp_tags:
                if t_item in tags_ct:
                    tags_ct[t_item] += 1
                else:
                    tags_ct.update({t_item:1})
        if 'CEO' in company_data['data']:
            comp_ceo = company_data['data']['CEO']
        if 'industry' in company_data['data']:
            comp_industry = company_data['data']['industry']
        if 'sector' in company_data['data']:
            comp_sector = company_data['data']['sector']
            if comp_sector in sector_ct:
                sector_ct[comp_sector] += 1
            else:
                sector_ct.update({comp_sector:1})
        if 'issueType' in company_data['data']:
            comp_issueType = company_data['data']['issueType']
            if comp_issueType in issueType_ct:
                issueType_ct[comp_issueType] += 1
            else:
                issueType_ct.update({comp_issueType:1})
        if 'website' in company_data['data']:
            comp_website = company_data['data']['website']
        if 'country' in company_data['data']:
            comp_country = company_data['data']['country']
            if comp_country in country_ct:
                country_ct[comp_country] += 1
            else:
                country_ct.update({comp_country:1})
        if sp_ct < 10:
            print(sp_ct, sk_symbol, comp_ceo, comp_employees, comp_tags, comp_industry, 
            comp_sector, comp_issueType, comp_website, comp_country)
    print('\n\n country_ct: ' + str(country_ct))
    print('\n\n issueType_ct: ' + str(issueType_ct))
    print('\n\n sector_ct: ' + str(sector_ct))
    print('\n\n tags_ct: ' + str(tags_ct))
    

def main():
    list_all_company_info_basic()

  
if __name__== "__main__":
    main()
