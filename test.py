# This script is used to try out the general features from nemosis library, also available in their README.md file on their GitHub page: 

from nemosis import defaults, dynamic_data_compiler

# print(defaults.dynamic_tables)

start_time = "2025/01/01 00:00:00"
end_time = "2025/01/01 00:05:00"
table = "DISPATCHPRICE"
raw_data_cache = "./raw_data_cache"

price_data = dynamic_data_compiler(start_time, end_time, table, raw_data_cache,
                                    filter_cols=['REGIONID'], filter_values=[['VIC1']])


unit_dispatch_data = dynamic_data_compiler(start_time, end_time, 'DISPATCHLOAD', raw_data_cache,
                                           filter_cols=['DUID', 'INTERVENTION', 'REGIONID'],
                                           filter_values=(['GSTONE1', 'HDWF2'], [0], ['VIC1']))
print(unit_dispatch_data)

# print(defaults.table_columns['DISPATCHPRICE'])