'''
This script visualise the price trough caused by solar during the day.
Focusing on data between 2025/01/01 and 2025/01/31 in Victoria.
'''

import nemosis

# Download the data
start_time = "2025/01/01 00:00:00"
end_time = "2025/01/31 23:55:00"
table = "DISPATCHPRICE"
raw_data_cache = "./raw_data_cache"

price_data = nemosis.dynamic_data_compiler(start_time, end_time, table, raw_data_cache,
                                            select_columns=['SETTLEMENTDATE', 'REGIONID','RRP'],
                                            filter_cols=['REGIONID'], filter_values=[['VIC1']])

# print(price_data)

